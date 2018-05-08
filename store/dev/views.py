from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from downloadapp.models import Package

from .forms import PackageForm

@login_required	
def dev_index(request):
	packages = Package.objects.order_by("date_changed").filter(owner=request.user)
	context = {'packages':packages}
	return render(request, 'dev/dev_index.html', context)
	
@login_required
def quick_check(request):
	return render(request, "dev/quick_check.html")

@login_required
def new_package(request):
	if request.method == 'POST':
		form = PackageForm(request.POST, request.FILES)
		if form.is_valid():
			new_package = form.save(commit=False)
			new_package.owner = request.user
			new_package.save()
			messages.success(request, "Your package have been submitted for certification.")
			return HttpResponseRedirect('/dev/')

	else:
		form = PackageForm()

	return render(request, 'dev/new_package.html', {'form': form})
	
def documentation_r(request):
	return render(request, 'dev/docs/rules.html')

def documentation_t(request):
	return render(request, 'dev/docs/tools.html')
