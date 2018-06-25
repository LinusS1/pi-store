from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile

class ProfileModelTest(TestCase):
	"""Test the Profile Model"""
	
	def setUp(self):
		self.test_user = User.objects.create(username="TestProfile", password="TestProfile")
		self.test_profile = Profile.objects.get(id=self.test_user.id)
	
	def test_profile_creation(self):
		"""Test __str__() - accounts"""
		self.assertTrue(isinstance(self.test_profile, Profile))
		self.assertEqual(self.test_profile.__str__(), self.test_profile.user.username)
