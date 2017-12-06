from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import PackageForm

@login_required
def new_package(request):
	if request.method == 'POST':
		form = PackageForm(request.POST, request.FILES)
		if form.is_valid():
			new_package = form.save(commit=False)
			new_package.owner = request.user
			new_package.save()
			return HttpResponseRedirect('/explore')

	else:
		form = PackageForm()

	return render(request, 'dev/new_package.html', {'form': form})
