from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from .models import Chapters, Profile, Lectures, Lectures_text, Image
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ChaptersForm(forms.ModelForm):
    class Meta:
        model = Chapters
        fields = ['title', 'description']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data        
        if cd['password'] != cd['password2']:            
            raise forms.ValidationError('Passwords don\'t match.')        
        return cd['password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo']

class LecturesForm(forms.ModelForm):

    class Meta:
        model = Lectures
        fields = ['name', 'value']

class LecturesTextForm(forms.ModelForm):

    class Meta:
        model = Lectures_text
        fields = ['lectures_id', 'title', 'text', 'photo']


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')

