import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    posts = Post.objects.all()[::-1]
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def posting(request):
    post = Post(poster=request.user, content=request.POST["content"])
    post.save()
    return HttpResponseRedirect(reverse("index"))


def edit(request, id):
    post = Post.objects.get(pk=id)
    post.content = request.POST["content"]
    post.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def profile(request, user_id):
    # Get all profile owner posts
    posts = Post.objects.filter(poster_id=user_id)[::-1]
    profile = User.objects.get(pk=user_id)
    return render(request, 'network/profile.html', {
        "posts": posts,
        "profile": profile
    })

@csrf_exempt
def follow_handler(request):
    if request.method == 'POST':
        # Get data from request
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        # Get profile owner and current user
        profile = User.objects.get(pk=profile_id)
        user = User.objects.get(username=request.user)
        # Check if current user in profile owner followers
        if user in profile.followers.all():
            # Remove user from followers
            profile.followers.remove(user)
            user.following.remove(profile)
        else:
            # Add user to followers
            profile.followers.add(user)
            user.following.add(profile)
        # Save changes
        profile.save()
        user.save()
        return JsonResponse({"profile": profile, "status": 200})
    else:
        return JsonResponse({"error": "Method is not POST", "status": 400})

@csrf_exempt
def like_handler(request):
    if request.method == 'POST':
        # Get data from the reuest
        data = json.loads(request.body)
        id = data.get('id')
        # Get post and user
        post = Post.objects.get(pk=id)
        user = request.user
        # Check if post is liked by the user
        if user in post.likes.all():
            # Remove user from likes query set
            post.likes.remove(user)
        else:
            # Add user to likes query set
            post.likes.add(user)
        # Save changes
        post.save()
        likecount = len(post.likes.all())
        return JsonResponse({"likecount": likecount, "status": 200})
    else:
        return JsonResponse({"error": "Method is not POST", "status": 400})




