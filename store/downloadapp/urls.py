from django.conf.urls import url

from . import views

app_name = 'downloadapp'
urlpatterns = [
	#Home
	url(r'^$', views.index, name='index'),
	#Welcome page
	url(r'^welcome$', views.welcome, name='welcome'),
	#Explore
	url(r'^explore$', views.explore, name='explore'),
	#Specific package
	url(r'^package/(?P<package_id>\d+)/$', views.package, name='package'),
	#Download package
	url(r'^package/download/(?P<package_id>\d+)/$', views.download, name='download'),
	#Manage
	url(r'^manage$', views.manage, name='manage'),
	#Download uninstall file
	url(r'^manage/uninstall/(?P<package_id>\d+)/$', views.uninstall, name='uninstall'),
	]
