from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
  user = models.OmeToOneField(User, related_name='profile')
  image = CloudinaryField('image')