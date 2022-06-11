from django.urls import path
from .views import *

urlpatterns = [
  path('',index, name='index'),
  path('accounts/', include('registration.backends.simple.urls')),
]