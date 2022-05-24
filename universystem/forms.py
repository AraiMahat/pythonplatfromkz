from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from .models import Chapters, Profile, Lectures, Lectures_text, Image
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.core.exceptions import ValidationError 
from django.forms.fields import EmailField 
from django.forms.forms import Form 
 
class CustomUserCreationForm(UserCreationForm): 
    username = forms.CharField(label='username', min_length=5, max_length=150) 
    email = forms.EmailField(label='email') 
    password1 = forms.CharField(label='password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput) 
 
    def username_clean(self): 
        username = self.cleaned_data['username'].lower() 
        new = User.objects.filter(username = username) 
        if new.count(): 
            raise ValidationError("User Already Exist") 
        return username 
 
    def email_clean(self): 
        email = self.cleaned_data['email'].lower() 
        new = User.objects.filter(email=email) 
        if new.count(): 
            raise ValidationError(" Email Already Exist") 
        return email 
 
    def clean_password2(self): 
        password1 = self.cleaned_data['password1'] 
        password2 = self.cleaned_data['password2'] 
 
        if password1 and password2 and password1 != password2: 
            raise ValidationError("Password don't match") 
        return password2 
 
    def save(self, commit = True): 
        user = User.objects.create_user( 
            self.cleaned_data['username'], 
            self.cleaned_data['email'], 
            self.cleaned_data['password1'] 
        ) 
        return user 
        
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

