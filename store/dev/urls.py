from django.conf.urls import url, include

from . import views

app_name = 'dev'
urlpatterns = [
	#Main developer page
	url(r'^$', views.dev_index, name='dev_index'),
	#New package
	url(r'^new/$', views.new_package, name='new_package'),
	#Documentation
	url(r'^dev/docs/rules/$', views.documentation_r, name='docs_r'),
	url(r'^dev/docs/tools/$', views.documentation_t, name='docs_t'),
	]
