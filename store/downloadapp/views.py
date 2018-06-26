from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime

from wsgiref.util import FileWrapper
import io as StringIO

from .models import Package

def user_date_today(user):
	now = datetime.datetime.now()
	return (now.date() - user.date_joined.date()).days

def index(request):
	if request.user.is_authenticated():
		user_joined = User.objects.get(id=request.user.id)
		if user_date_today(user_joined) <= 7:
			user_joined = True
		else:
			user_joined = False
	else:
		user_joined = True
	
	packages = Package.objects.order_by("date_changed").filter(stage='LIV')[:5]
	
	context = {'user_joined':user_joined, 'packages':packages}
	return render(request, 'downloadapp/index.html', context)

def welcome(request):
	return render(request, 'downloadapp/welcome.html')

def explore(request):
	"""Main way to find packages"""
	packages = Package.objects.order_by("date_changed").filter(stage='LIV')
	context = {'packages':packages}
	return render(request, 'downloadapp/explore.html', context)

def package(request, package_id):
	"""Specific package"""
	package = get_object_or_404(Package, pk=package_id)
	if request.user.is_authenticated():
		user = User.objects.get(id=request.user.id)
		if user.profile.installed_packages.filter(pk=package_id).exists():
			has_package = True
		else:
			has_package = False
	else:
		has_package = False
	context = {'package':package, 'has_package':has_package}
	return render(request, 'downloadapp/package.html', context)

def add_package_to_profile(user, package):
	user.profile.installed_packages.add(package)
	user.save()

@login_required
def download(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	#Add on to database
	Package.objects.filter(id=package_id).update(installs=F('installs')+1)
	#Add to users package list
	user = User.objects.get(id=request.user.id)
	add_package_to_profile(user, package)
	context = {"package":package}
	return render(request, 'downloadapp/download.html', context)

@login_required
def manage(request):
	packages_installed = []
	user = User.objects.get(id=request.user.id)

	#get all packages installed
	packages_installed = user.profile.installed_packages.all()
	#list all packages installed
	context = {'packages':packages_installed}
	return render(request, "downloadapp/manage_packages.html", context)

@login_required
def uninstall(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	#remove install count
	Package.objects.filter(id=package_id).update(installs=F('installs')-1)
	#remove from profile
	user = User.objects.get(id=request.user.id)
	user.profile.installed_packages.remove(package)
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
