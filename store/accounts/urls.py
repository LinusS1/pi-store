"""URL patterns for accounts"""
from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'accounts'
urlpatterns = [
	#Privacy
	url(r'^private/$', views.private, name="private"),
	#TOS
	url(r'^tos/$', views.tos, name="tos"),
	]
