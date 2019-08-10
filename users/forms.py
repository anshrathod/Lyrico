from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	fname=forms.CharField(label='Firstname')
	lname=forms.CharField(label='Lastname')

	class Meta:
		model = User
		fields = ['fname','lname','email','username','password1','password2']

	def save(self,commit=True):
		user = super(UserRegisterForm,self).save(commit=False)
		user.fname=self.cleaned_data.get('fname')
		user.lname=self.cleaned_data.get('lname')
		user.email=self.cleaned_data.get('email')
		if commit :
			user.save()
		return user