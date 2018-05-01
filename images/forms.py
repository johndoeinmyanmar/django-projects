from urllib import request
from django.core.files.base import ContentFile
from django import forms
from .models import Image
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		widgets = {
			'url' : forms.HiddenInput, 
		}


	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extensions = url.rsplit('.', 1)[1].lower()
		if extensions not in valid_extensions:
			raise forms.ValidationError('Invalid image file type...')

		return url 


	def save(self, force_insert=False, force_update=False, commit=True):

		image = super(ImageCreateForm, self).save(commit=False)
		image_url = self.cleaned_data['url']
		image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())

		# download image from the given url
		respond = request.urlopen(image_url)
		image.image.save(image_name, ContentFile(respond.read()), save=False)

		if commit:
			image.save()

		return image 