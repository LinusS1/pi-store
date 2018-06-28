from django.shortcuts import render

def private(request):
	return render(request, "accounts/private.html")
	
def tos(request):
	return render(request, "accounts/tos.html")
