from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from markdownx.utils import markdownify
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from smartfile import BasicClient
from decouple import config
from django.contrib.auth.models import User
import time
import pdb

from .views import add_package_to_profile
from .models import Package
from accounts.models import Profile
from .storage import saveSmartFileShot, saveSmartFileSoft

class PackageModelTest(TestCase):
	"""Test the model downloadapp."""
	
	def setUp(self):
		"""Create a package to test"""
		self.test_package = Package.objects.create(name="Test Package", description="Really, just a ***test*** package!",\
			simple_description="Test Package", shot=SimpleUploadedFile("test_shot.png", b"image/png", content_type="image/png"),\
			catagory="APP", software=SimpleUploadedFile("test_package_soft.zip", b"application/zip", "application/zip"))
		# Access to the api
		self.api = BasicClient(config('SMARTFILE_API_KEY'),config('SMARTFILE_API_PASSWORD'))
		
	def test_formatted_markdown(self):
		"""Test formatted markdown function"""
		self.assertEqual(markdownify(self.test_package.description), self.test_package.formatted_markdown())
		
	def test_package_creation(self):
		"""Test __str__()"""
		self.assertTrue(isinstance(self.test_package, Package))
		self.assertEqual(self.test_package.__str__(), self.test_package.name)
	
	def tearDown(self):
		"""Delete the files stored"""
		#Delete Screen Shot
		self.api.post("/path/oper/remove/", path="/screenShot/test_shot.png")
		# Delete package
		self.api.post("/path/oper/remove/", path="/software/test_package_soft.zip")

class StorageTest(TestCase):
	"""Test the package saving and retrieving system"""
	
	def setUp(self):
		"""Add access to the api"""
		self.api = BasicClient(config('SMARTFILE_API_KEY'),config('SMARTFILE_API_PASSWORD'))
		#Make software file, call _save
		self.software = saveSmartFileSoft._save(self, "test_package_soft.zip", SimpleUploadedFile("test_package_soft.zip", b"application/zip", "application/zip"))

		#Make screen shot file, call _save
		self.shot = saveSmartFileShot._save(self, "test_shot.png", SimpleUploadedFile("test_shot.zip", b"image/png", "image/png"))
	
	def test_smartfile_connectivity(self):
		"""Test if smartfile is online"""
		self.assertEqual(self.api.get('/ping'), {"ping": "pong"})
		
	def test_software_save(self):
		"""Test the uploading of software"""
		#Check return of function _save
		self.assertEqual(self.software, "/software/test_package_soft.zip")
		#Check upload of function _save
		response = self.api.get("/path/info/software/test_package_soft.zip")
		response = response['isfile']
		self.assertEqual(response, True)
		
	def test_software_open(self):
		"""Test the _open function of software"""
		data = self.api.get('/path/data/software/test_package_soft.zip')
		self.assertEqual(data.read(), saveSmartFileSoft._open(self, "test_package_soft.zip").read())
		
	def test_software_get_aviable_name(self):
		"""Test the get_aviable name function"""
		self.assertEqual("Test Package Name", saveSmartFileSoft.get_available_name(self, "Test Package Name"))
		
	def test_software_url(self):
		"""Test the URL generator"""
		self.assertEqual("https://file.ac/nrNWC7hRM7Y//software/test_package_soft.zip", saveSmartFileSoft.url(self, "/software/test_package_soft.zip"))
	
	###  Tests for smartfileShot  ####
	def test_shot_save(self):
		"""Test the uploading of screen shots"""
		#Check return of function _save
		self.assertEqual(self.shot, "/screenShot/test_shot.png")
		#Check upload of function _save
		response = self.api.get("/path/info/screenShot/test_shot.png")
		response = response['isfile']
		self.assertEqual(response, True)
		
	def test_shot_open(self):
		"""Test the _open function of screen shots"""
		data = self.api.get('/path/data/screenShot/test_shot.png')
		self.assertEqual(data.read(), saveSmartFileShot._open(self, "test_shot.png").read())
		
	def test_shot_get_aviable_name(self):
		"""Test the get_aviable name function screen shots"""
		self.assertEqual("Test Screen Shot Name", saveSmartFileShot.get_available_name(self, "Test Screen Shot Name"))
		
	def test_shot_url(self):
		"""Test the URL generator screen shots"""
		self.assertEqual("https://file.ac/FUt50I5XH8U//screenShot/test_shot.png", saveSmartFileShot.url(self, "/screenShot/test_shot.png"))
		
	def tearDown(self):
		"""Delete the files stored"""
		#Delete Screen Shot
		self.api.post("/path/oper/remove/", path="/screenShot/test_shot.png")
		# Delete package
		self.api.post("/path/oper/remove/", path="/software/test_package_soft.zip")

class ViewsTest(TestCase):
	"""Test the views in downloadapp"""
	
	def setUp(self):
		"""Create 2 packages: one live one in certification"""
		
		self.api = BasicClient(config('SMARTFILE_API_KEY'),config('SMARTFILE_API_PASSWORD'))
		self.factory = RequestFactory()
		
		self.test_package = Package.objects.create(name="Test Package", description="Really, just a ***test*** package!",\
			simple_description="Test Package", shot=SimpleUploadedFile("test_shot.png", b"image/png", content_type="image/png"),\
			catagory="APP", software=SimpleUploadedFile("test_package_soft.zip", b"application/zip", "application/zip"), stage='LIV')
			
		self.cert_test_package = Package.objects.create(name="Cert Test Package", description="Really, just a ***test*** package! In cert mode.",\
			simple_description="Test Cert Package", shot=SimpleUploadedFile("test_cert_shot.png", b"image/png", content_type="image/png"),\
			catagory="APP", software=SimpleUploadedFile("test_cert_package_soft.zip", b"application/zip", "application/zip"))
		
		#Create a user with a package installed
		self.userInstalled = User.objects.create(username="TestUserInstalled", password="TestUserInstalled")
		self.userInstalled.profile.installed_packages.add(self.test_package)
		
		#Create a user with a package not installed
		self.userNotInstalled = User.objects.create(username="TestUser", password="TestUser")
		#~ self.userNotInstalled.profile.installed_packages.add(self.test_package)
		
	def test_index_view(self):
		"""Test the index view"""
		url = reverse("downloadapp:index")
		resp = self.client.get(url)
		
		self.assertEqual(resp.status_code, 200)
		self.assertIn(b"Pi Store", resp.content)
		
	def test_explore_view(self):
		"""Test the explore views"""
		url = reverse("downloadapp:explore")
		resp = self.client.get(url)
		#Make sure Test package is served
		self.assertQuerysetEqual(resp.context["packages"], ["<Package: Test Package>"])
	
	def test_package_view(self):
		"""Test the package view"""
		self.client.force_login(self.userNotInstalled, backend="allauth")
		resp = self.client.get("/package/1/")
		# Test that user without package can download
		self.assertIn(b"Download", resp.content)
		self.client.logout()
		# Test that user with package gets managed
		self.client.force_login(self.userInstalled, backend="allauth")
		resp = self.client.get("/package/1/")
		self.assertIn(b"Manage", resp.content)
		self.client.logout()
	
	def test_download_view(self):
		"""Test that the package is added to the users profile"""
		add_package_to_profile(self.userNotInstalled, self.test_package)
		self.assertTrue(self.test_package, self.userNotInstalled.profile.installed_packages.all())
	
	def test_manage_view(self):
		"""Test that profile packages in context"""
		self.client.force_login(self.userInstalled, backend="allauth")
		resp = self.client.get("/manage")
		#~ pdb.set_trace()
		self.assertIn(self.test_package, self.userInstalled.profile.installed_packages.all())
		self.client.logout()
	
	def test_uninstall_view(self):
		"""Test the response of the uninstall view and the remove of the package."""
		self.client.force_login(self.userInstalled, backend="allauth")
		resp = self.client.get("/manage/uninstall/{}/".format(self.test_package.id))
		#Test that package is removed from profile
		self.assertNotIn(self.test_package.name, self.userInstalled.profile.installed_packages.all())
		#Re add package
		self.userInstalled.profile.installed_packages.add(self.test_package)
		self.client.logout()
		
	def tearDown(self):
		"""Delete the files stored"""
		#Delete Screen Shots
		self.api.post("/path/oper/remove/", path="/screenShot/test_shot.png")
		self.api.post("/path/oper/remove/", path="/screenShot/test_cert_shot.png")
		# Delete packages
		self.api.post("/path/oper/remove/", path="/software/test_package_soft.zip")
		self.api.post("/path/oper/remove/", path="/software/test_cert_package_soft.zip")
