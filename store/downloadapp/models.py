from django.db import models
from .storage import saveSmartFileDisp, saveSmartFileSoft


class Package(models.Model):
	"""The downloadable package."""
	name = models.CharField(max_length=200)# Name of the app
	description = models.TextField()
	date_changed = models.DateTimeField(auto_now_add=True)# when the app was last changed/added.
	# display image
	display = models.ImageField(max_length=200, storage=saveSmartFileDisp())
	#published?
	isPublished = models.BooleanField(default=False)
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
	
	def __str__(self):
		return self.name
