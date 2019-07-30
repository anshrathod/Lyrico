from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 
from django.contrib import messages
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	fname=forms.CharField(label='Firstname')
	lname=forms.CharField(label='Lastname')

	class Meta:
		model = User
		fields = ['fname','lname','email','username','password1','password2']

	def save(self,commit=True):
		user = super(UserRegisterForm,self).save(commit=False)
		user.firstname=self.cleaned_data['fname']
		user.lname=self.cleaned_data['lname']
		user.email= self.cleaned_data['email']
		if commit :
			user.save()
		return user


class UserUpdateForm(forms.ModelForm):
	fname=forms.CharField(label='Firstname')
	lname=forms.CharField(label='Lastname')
	class Meta:
		model=User
		fields=['fname','lname']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model=Profile
		fields=['image',
				'bio',
    			'age',
    			'gender']