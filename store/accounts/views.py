from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('downloadapp:index'))
