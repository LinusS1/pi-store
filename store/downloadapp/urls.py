from django.conf.urls import url

from . import views

app_name = 'downloadapp'
urlpatterns = [
	#Home
	url(r'^$', views.index, name='index'),
	#Explore
	url(r'^explore$', views.explore, name='explore'),
	#Specific package
	url(r'^package/(?P<package_id>\d+)/$', views.package, name='package'),
	#Download package
	url(r'^package/download/(?P<package_id>\d+)/$', views.download, name='download'),
	#New package
	url(r'^dev/packages/new$', views.new, name='new'),
	]
