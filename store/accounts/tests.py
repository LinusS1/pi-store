from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile

class ProfileModelTest(TestCase):
	"""Test the Profile Model"""
	
	def setUp(self):
		self.test_profile = User.objects.create(username="TestProfile", password="TestProfile")
	
	def test_profile_creation(self):
		"""Test __str__()"""
		self.assertTrue(isinstance(self.test_profile, User))
		self.assertEqual(self.test_profile.__str__(), self.test_profile.username)
