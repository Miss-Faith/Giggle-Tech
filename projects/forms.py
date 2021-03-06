from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

from cloudinary.models import CloudinaryField

def ForbiddenUsers(value):
  forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
  'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
  if value.lower() in forbidden_users:
    raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
  if '@' in value or '+' in value or '-' in value:
    raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
  if User.objects.filter(email__iexact=value).exists():
    raise ValidationError('User with this email already exists.')

def UniqueUser(value):
  if User.objects.filter(username__iexact=value).exists():
    raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
  username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=30, required=True,)
  email = forms.CharField(label='',widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=100, required=True,)
  password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  confirm_password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True)

  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators.append(ForbiddenUsers)
    self.fields['username'].validators.append(InvalidUser)
    self.fields['username'].validators.append(UniqueUser)
    self.fields['email'].validators.append(UniqueEmail)

  def clean(self):
    super(SignupForm, self).clean()
    password = self.cleaned_data.get('password')
    confirm_password = self.cleaned_data.get('confirm_password')

    if password != confirm_password:
      self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
    return self.cleaned_data

class NewPostForm(forms.ModelForm):
  title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Project Name','class': 'input is-medium'}), required=True)
  image = forms.FileField(label='',widget=forms.ClearableFileInput(attrs={'placeholder': 'Image','class': 'textarea','multiple': False}), required=True)
  description = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Project Description','class': 'input is-medium'}), required=True)
  technologies = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Technologies used','class': 'input is-medium'}), required=True)
  url = forms.URLField(label='',widget=forms.TextInput(attrs={'placeholder': 'Github Url','class': 'input is-medium'}), required=True)

  class Meta:
    model = Post
    fields = ('title', 'image', 'description', 'technologies', 'url')


class UpdateUserProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['firstname', 'lastname', 'picture', 'bio']

class RatingsForm(forms.ModelForm):
  class Meta:
    model = Rating
    fields = ['design', 'usability', 'content']