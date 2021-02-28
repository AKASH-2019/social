from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile, Follow
from django.contrib.auth.models import User

from App_Posts.models import Post, Like

# Create your views here.
@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))   # posts <- upload date
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)

    return render(request, 'App_Posts/home.html', context={'title': 'home', 'search': search, 'result': result,
                                                           'posts': posts, 'liked_post_list':liked_post_list})

    # return render(request, 'App_Posts/home.html', context={'title': 'home', 'search': search, 'result': result,
    #                                                         'following_list': following_list})

#  home.html

        # {% for author in following_list %}
        # {% for post in author.following.post.all %}
        # <div style="border: 1px solid #808080;">
        #    <div style="padding: 10px">
        #        {% if post.author.user_profile.profile_pic %}
        #           <img src="/media/{{ post.author.user_profile.profile_pic }}"width="50px" height="50px" class="rounded-circle">
        #        {% else %}
        #           <img src="/media/def_img.jpeg/"width="50px" height="50px" class="rounded-circle">
        #        {% endif %}
        #        <a href="{% url 'App_Login:user' username=post.author %}">{{post.author}}</a>
        #    </div>
        #    <img src="/media/{{post.image}}" width="100%">
        # </div>
        # <br>
        # <br>
        # {% endfor %}
        # {% endfor %}

@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))



