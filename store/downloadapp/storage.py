from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from smartfile import BasicClient

@deconstructible
class saveSmartFileDisp(Storage):
	"""Save things using smart file using django"""
	
	def __init__(self):
		self.api = BasicClient()
		testA = self.api.get('/ping')
		
	def _open(self, name, mode='rb'):
		Refile = self.api.get('path/data/displayImg/{0}'.format(name))
		return Refile
	
	def _save(self, name, content):
		self.api.upload(name, content)
		self.api.move(name, '/displayImg')
		return "/displayImg/"+name

	def get_available_name(self, name, max_length=None):
		return name
		
	def url(self, name):
		#parse url
		return "https://file.ac/fgazR9q1Y7M/"+name
		
@deconstructible
class saveSmartFileSoft(Storage):
	"""Save things using smart file using django"""
	
	def __init__(self):
		self.api = BasicClient()
		testA = self.api.get('/ping')
		
	def _open(self, name, mode='rb'):
		Refile = self.api.get('path/data/software/{0}'.format(name))
		return Refile
	
	def _save(self, name, content):
		self.api.upload(name, content)
		self.api.move(name, '/software')
		#create url
		return "/software/"+name

	def get_available_name(self, name, max_length=None):
		return name
		
	def url(self, name):
		#parse url
		return "https://file.ac/nrNWC7hRM7Y/"+name
