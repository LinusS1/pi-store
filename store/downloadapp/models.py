from django.db import models
from .storage import saveSmartFileSoft, saveSmartFileShot
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Package(models.Model):
	"""The downloadable package."""
	name = models.CharField(max_length=200)# Name of the app
	description = MarkdownxField()
	simple_description = models.CharField(max_length=300, null=True, blank=False)
	date_changed = models.DateTimeField(auto_now_add=True)# when the app was last changed/added.
	# display image
	shot = models.ImageField(max_length=200, storage=saveSmartFileShot())
	#catagory
	CATAGORY_CHOICES = (
		('GAM', 'Games'),
		('APP', 'Apps'),
		('DEV', 'Devloper tools'),
		('MED', 'Media'),
	)
	catagory = models.CharField(
		max_length=3,
		choices=CATAGORY_CHOICES,
		default='APP',
	)
	#The software... Finally!
	software =  models.FileField(storage=saveSmartFileSoft())
	installs = models.IntegerField(default=2)
	owner = models.ForeignKey(User, null=True, blank=False)
	#What stage the package is in
	STAGE_CHOICES = (
		('LOK', 'Certification'),
		('LIV', 'Live!'),
	)
	stage = models.CharField(
		max_length=3,
		choices=STAGE_CHOICES,
		default='LOK',
	)
	message = models.TextField(null=True, blank=False)
	
	def formatted_markdown(self):
		return markdownify(self.description)
	
	def __str__(self):
		return self.name
