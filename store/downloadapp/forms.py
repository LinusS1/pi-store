from django import forms

from .models import Package

class PackageForm(forms.ModelForm):
	#~ name = forms.CharField(max_length=200, label="Name of package: ")
	#~ description = forms.CharField(widget=forms.Textarea, label="Description of package: ")
	#~ CHOICES = (
		#~ ('GAM', 'Games'),
		#~ ('APP', 'Apps'),
		#~ ('DEV', 'Devloper tools'),
		#~ ('MED', 'Media'),
	#~ )
	#~ catagory = forms.MultipleChoiceField(choices=CHOICES, label="Choose the catagory your package fits into." )
	#~ software = forms.FileField(label="The software package. Must be compressed into a zip file. ")
	#~ display = forms.ImageField(label="The display image. Try to keep the file size small.")# the display image
	#~ shot = forms.ImageField(label="The screen shot")# screen shot
	
	class Meta:
		model = Package
		fields = ['name', 'description', 'catagory', 'software', 'display', 'shot']
