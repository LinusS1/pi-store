"""URL patterns for accounts"""
from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'accounts'
urlpatterns = [
	#Login
	url(r'^login/$', login, {'template_name':'accounts/login.html'}, name='login'),
	#logout
	url(r'^logout/$', views.logout_view, name="logout"),
	]
