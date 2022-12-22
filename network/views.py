import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


# Paginate (divide output by pages)
def paginate(request, listing): 
    paginator = Paginator(listing, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    # Get all posts in reverse chronological order
    posts = Post.objects.all()[::-1]
    # Paginate
    page_obj = paginate(request, posts)
    return render(request, "network/index.html", {
        "page_obj": page_obj
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
    if request.method == 'POST':
        # Create a new post using the form data and save it
        post = Post(poster=request.user, content=request.POST["content"])
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Error: Method is not POST.")


def following(request):
    # Get current user
    user = User.objects.get(pk=request.user.id)
    # Obtain posts of all users the current user follows
    posts_following = []
    for followed in user.following.all():
        posts = Post.objects.filter(poster=followed)
        posts_following.extend(posts)
    # Sort all obtained posts in reverse chronological order
    posts_following = sorted(posts_following, key = lambda post: post.id, reverse=True)
    page_obj = paginate(request, posts_following)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@csrf_exempt
def edit(request):
    if request.method == 'POST':
        # Get request data
        data = json.loads(request.body)
        id = data.get('id')
        edited = data.get('edited')
        # Get the post to be edited
        post = Post.objects.get(pk=id)
        # Edit post content and save changes
        post.content = edited
        post.save()
        # Return to the function calling page
        content = post.content
        return JsonResponse({"content": content})
    else:
        return HttpResponse("Error: Method is not POST.")

@login_required
def profile(request, user_id):
    # Get all profile owner posts
    posts = Post.objects.filter(poster_id=user_id).order_by('-id')
    # Paginate
    page_obj = paginate(request, posts)
    # Get the profile query set
    profile = User.objects.get(pk=user_id)
    return render(request, 'network/profile.html', {
        "page_obj": page_obj,
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
        user = User.objects.get(pk=request.user.id)
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
        # Count followers
        followercount = profile.followers.count()
        profilename = profile.username.capitalize()
        return JsonResponse({"followercount": followercount, "profilename": profilename})
    else:
        return HttpResponse("Error: Method is not POST.")

@login_required
@csrf_exempt
def like_handler(request):
    if request.method == 'POST':
        # Get data from the request
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
        # Count likes
        likecount = post.likes.count()
        return JsonResponse({"likecount": likecount})
    else:
        return HttpResponse("Error: Method is not POST.")




