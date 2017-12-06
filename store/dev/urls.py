from django.conf.urls import url

from . import views

app_name = 'dev'
urlpatterns = [
	#New package
	url(r'^packages/new$', views.new_package, name='new_package'),
	]
