from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete
import datetime as dt

from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  bio = models.TextField(max_length=150)
  picture = CloudinaryField('picture')

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    SIZE = 250, 250

  def __str__(self):
    return self.user.username

  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(user=instance)

  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

  post_save.connect(create_user_profile, sender=User)
  post_save.connect(save_user_profile, sender=User)

class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=120, null=True, blank=False)
  image = CloudinaryField('image')
  description = models.TextField(max_length=1200, blank=False, verbose_name='Description')
  posted = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rates = models.IntegerField(default=0)

  def __str__(self):
    return str(self.id)

  @classmethod
  def search_post(cls, search_term):
    projects = cls.objects.filter(post__name__icontains=search_term)
    return projects

  def add_post(self):
    self.save()


class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def user_save_comment_post(sender, instance, *args, **kwargs):
    comment = instance
    post = comment.post
    text_preview = comment.body[:90]
    sender = comment.user

  def user_del_comment_post(sender, instance, *args, **kwargs):
    comment = instance
    post = comment.post
    text_preview = comment.body[:90]
    sender = comment.user

post_save.connect(Comment.user_save_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)

class Rate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rate')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_rate')

  def user_rated_post(sender, instance, *args, **kwargs):
    rate = instance
    post = rate.post
    sender = rate.user

post_save.connect(Rate.user_rated_post, sender=Rate)