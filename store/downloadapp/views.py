from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
	user = User.objects.get(id=request.user.id)
	if user.profile.packages_installs != None and str(package.id) in list(user.profile.packages_installs.split(",")):
		has_package = True
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
