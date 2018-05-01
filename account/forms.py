from django import forms
from django.contrib.auth.models import User 
from .models import Profile, Item 



class UserRegistrationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'type':'password','_class':'form-control','id':'passwd'}))
	password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'type':'password','_class':'form-control','id':'passwd'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')
		labels = {
			'email': ('Email'),
		}
		widgets = {
			'username' : forms.TextInput(attrs={'type':'text','_class':'form-control', 'id':'name'}),
			'first_name' : forms.TextInput(attrs={'type':'text','_class':'form-control','id':'name'}),
			'email' : forms.TextInput(attrs={'type':'email','_class':'form-control', 'id':'email'}),

		}

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Password don\'t match...')
		return cd['password2']


class UserEditForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):

	class Meta:
		model = Profile 
		fields = ('phone', 'photo','location')

class ItemShareForm(forms.ModelForm):

	class Meta:
		model = Item 
		fields = ('title', 'cover', 'link', 'description', 'status', 'item')

		widgets = {
			'description' : forms.Textarea(),
			}

