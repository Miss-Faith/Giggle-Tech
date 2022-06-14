from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.template import loader
import random

# Create your views here.
def index(request): 
  posts = Post.objects.all().order_by('-posted')
  #   a_post = random.randint(0, len(posts)-1)	
  #   random_post = posts[a_post]

  if request.method == "POST":
      form = NewPostForm(request.POST)
      if form.is_valid():
          post = form.save(commit=False)
          post.user = request.user
          post.save()
  else:
      form = NewPostForm()

  template = loader.get_template('index.html')
  context = {
    'posts': posts,
    'form':form,
    # 'random_post':random_post
  }

  return HttpResponse(template.render(context, request))

  return render(request, 'index.html')

def search_results(request):
    if request.method == 'GET':
        search_term = request.GET.get("project")
        searched_projects = Post.search_project(search_term)
        message = f"{search_term}"
        return render(request, 'search.html', {"message":message,"projects": searched_projects})
    else:
        message = "You haven't searched for any project"
    return render(request, 'search.html', {'message': message})

@login_required()
def project(request, post_id):
    post = Post.objects.get(id=post_id)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'project.html', params)

