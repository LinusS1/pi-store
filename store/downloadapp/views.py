from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Package

def index(request):
	return render(request, 'downloadapp/index.html')

def explore(request):
	"""Main way to find packages"""
	packages = Package.objects.order_by("date_changed").filter(isPublished = True)
	context = {'packages':packages}
	return render(request, 'downloadapp/explore.html', context)

def package(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	context = {'package':package}
	return render(request, 'downloadapp/package.html', context)

def download(request, package_id):
	package = get_object_or_404(Package, pk=package_id)
	#Add on to database
	Package.objects.filter(id=package_id).update(installs=F('installs')+1)
	context = {"package":package}
	return render(request, 'downloadapp/download.html', context)
