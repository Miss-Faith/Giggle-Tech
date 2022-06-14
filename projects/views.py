from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.template import loader

# Create your views here.

def index(request):
  user = request.user
 
  post_items = Post.objects.all().order_by('-posted')		
  template = loader.get_template('index.html')
  context = {
    'post_items': post_items,
  }

  return HttpResponse(template.render(context, request))

  return render(request, 'index.html')

def search_results(request):
    if 'post' in request.GET and request.GET["post"]:
        search_term = request.GET.get("post")
        searched_posts = Post.search_post(search_term)
        message = f"{search_term}"
        return render(request, 'search.html', {"message":message,"posts": searched_posts})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'search.html', {'message': message})