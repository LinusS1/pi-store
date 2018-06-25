from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from downloadapp.models import Package

class ViewsDevTests(TestCase):
	"""Test the dev views"""
	
	def setUp(self):
		"""Setup the env for dev views"""
		self.testDevUser = User.objects.create_user(username="TestDevUser", password="TestDevUser")
	
	def test_quick_check_view(self):
		"""Test the quick check view"""
		self.client.login(username="TestDevUser", password="TestDevUser", backend="allauth")
		resp = self.client.get("/dev/quick_check/")
		self.assertEqual(resp.status_code, 200)
		self.assertIn(b"quick check", resp.content)
		
	def test_documentation_r_view(self):
		"""Test the dev rules view"""
		resp = self.client.get("/dev/docs/rules/")
		
		self.assertEqual(resp.status_code, 200)
		self.assertIn(b"Rules", resp.content)
	
	def test_documentation_t_view(self):
		"""Test the dev tools view"""
		resp = self.client.get("/dev/docs/tools/")
		
		self.assertEqual(resp.status_code, 200)
		self.assertIn(b"Tools", resp.content)
	
	def test_dev_index_view(self):
		"""Test the dev index view"""
		self.client.login(username="TestDevUser", password="TestDevUser", backend="allauth")
		self.test_dev_package = Package.objects.create(owner=self.testDevUser, name="Test Package", description="Really, just a ***test*** package!",\
			simple_description="Test Package", shot=SimpleUploadedFile("test_shot.png", b"image/png", content_type="image/png"),\
			catagory="APP", software=SimpleUploadedFile("test_package_soft.zip", b"application/zip", "application/zip"), stage='LIV')
		
		resp = self.client.get("/dev/")
		self.assertEqual(resp.status_code, 200)
		self.assertIn(self.test_dev_package, resp.context['packages'])
	
	def test_new_package_view(self):
		"""Test the new package view"""
		self.client.login(username="TestDevUser", password="TestDevUser", backend="allauth")
		resp = self.client.get("/dev/new_package/")
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'dev/new_package.html')
		self.assertTrue(resp.context['form'])
