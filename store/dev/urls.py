from django.conf.urls import url, include

from . import views

app_name = 'dev'
urlpatterns = [
	#Main developer page
	url(r'^$', views.dev_index, name='dev_index'),
	#New package-assistant
	#Quick Check
	url(r'^quick_check/$', views.quick_check, name='quick_check'),
	#New Package
	url(r'^new_package/$', views.new_package, name='new_package'),
	#Documentation
	url(r'^docs/rules/$', views.documentation_r, name='docs_r'),
	url(r'^docs/tools/$', views.documentation_t, name='docs_t'),
	]
