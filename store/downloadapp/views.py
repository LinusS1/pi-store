from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string

from wsgiref.util import FileWrapper
import io as StringIO

from .models import Package
from .forms import PackageForm


def index(request):
	return render(request, 'downloadapp/index.html')

def explore(request):
	"""Main way to find packages"""
	packages = Package.objects.order_by("date_changed").filter(isPublished = True)
	context = {'packages':packages}
	return render(request, 'downloadapp/explore.html', context)

def package(request, package_id):
	"""Specific package"""
	package = get_object_or_404(Package, pk=package_id)
	if request.user.is_authenticated():
		user = User.objects.get(id=request.user.id)
		if user.profile.packages_installs != None and str(package.id) in list(user.profile.packages_installs.split(",")):
			has_package = True
		else:
			has_package = False
	else:
		has_package = False
	context = {'package':package, 'has_package':has_package}
	return render(request, 'downloadapp/package.html', context)

@login_required
def download(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	#Add on to database
	Package.objects.filter(id=package_id).update(installs=F('installs')+1)
	#Add to users package list
	user = User.objects.get(id=request.user.id)
	user.profile.packages_installs = str(user.profile.packages_installs).strip("None")+str(package_id)+","
	user.save()
	context = {"package":package}
	return render(request, 'downloadapp/download.html', context)
	
@login_required
def manage(request):
	packages_installed = []
	user_package_ids = User.objects.get(id=request.user.id)
	try:
		user_package_ids = list(user_package_ids.profile.packages_installs.split(","))
		packages_installed = []
		for n in user_package_ids:
			if n != '':
				packages_installed.append(Package.objects.get(id=n))
	except:
		pass
	context = {'packages':packages_installed}
	return render(request, "downloadapp/manage_packages.html", context)
	
@login_required
def uninstall(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	#remove install count
	Package.objects.filter(id=package_id).update(installs=F('installs')-1)
	#remove from profile
	user = User.objects.get(id=request.user.id)
	user_packages = list(user.profile.packages_installs.split(","))
	user.profile.packages_installs = user_packages.remove(str(package_id))
	user.save()
	#Get file ready
	t = render_to_string('downloadapp/uninstall_template.txt', context={'id':package_id})
	tFile = StringIO.StringIO()
	tFile.write(t)
	
	#Attach file to header
	#return uninstall template
	response = HttpResponse(tFile.getvalue(), content_type='application/plain')
	response['Content-Disposition'] = 'attachment; filename=uninstall.txt'
	return response
########################### DEVELOPER
@login_required
def new(request):
	if request.method == 'POST':
		form = PackageForm(request.POST, request.FILES)
		if form.is_valid():
			new_package = form.save(commit=False)
			new_package.owner = request.user
			new_package.save()
			return HttpResponseRedirect('/explore')

	else:
		form = PackageForm()

	return render(request, 'downloadapp/new_package.html', {'form': form})
