from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
  path('', index, name='index'),
  path('project/<post>', project, name='project'),
  path('signup/', signup, name='signup'),
  path('account/', include('django.contrib.auth.urls')),
  path('api/', include(router.urls)),
  path('<username>/profile', user_profile, name='userprofile'),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  path('profile/<username>/', profile, name='profile'),
  path('profile/<username>/settings', edit_profile, name='edit'),
  path('search/', search_project, name='search'),
]