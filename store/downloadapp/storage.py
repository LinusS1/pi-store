from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from smartfile import BasicClient
from decouple import config
		
@deconstructible
class saveSmartFileSoft(Storage):
	"""Save things using smart file using django"""
	
	def __init__(self):
		self.api = BasicClient(config('SMARTFILE_API_KEY'),config('SMARTFILE_API_PASSWORD'))
		testA = self.api.get('/ping')
		
	def _open(self, name, mode='rb'):
		Refile = self.api.get('path/data/software/{0}'.format(name))
		return Refile
	
	def _save(self, name, content):
		#Create what is getting sent
		arg = (name, content)
		#send the file and name off!
		self.api.post("/path/data/software/", file=arg)
		#create url
		return "/software/"+name

	def get_available_name(self, name, max_length=None):
		return name
		
	def url(self, name):
		#parse url
		return "https://file.ac/nrNWC7hRM7Y/"+name

		
@deconstructible
class saveSmartFileShot(Storage):
	"""Save things using smart file using django"""
	
	def __init__(self):
		self.api = BasicClient(config('SMARTFILE_API_KEY'),config('SMARTFILE_API_PASSWORD'))
		testA = self.api.get('/ping')
		
	def _open(self, name, mode='rb'):
		Refile = self.api.get('path/data/screenShot/{0}'.format(name))
		return Refile
	
	def _save(self, name, content):
		#Create what is getting sent
		arg = (name, content)
		#send the file and name off!
		self.api.post("/path/data/screenShot/", file=arg)
		#create url
		return "/screenShot/"+name

	def get_available_name(self, name, max_length=None):
		return name
		
	def url(self, name):
		#parse url
		return "https://file.ac/EWLnE13zcKA/"+name
