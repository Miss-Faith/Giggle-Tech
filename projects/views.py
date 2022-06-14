from django.shortcuts import render

# Create your views here.

def index(request):

  return render(request, 'index.html')

@login_required
def search_results(request):
    if 'post' in request.GET and request.GET["post"]:
        search_term = request.GET.get("post")
        searched_posts = Post.search_post(search_term)
        message = f"{search_term}"
        return render(request, 'search.html', {"message":message,"posts": searched_posts})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'search.html', {'message': message})