import json
import operator
from functools import reduce
from requests import get
from random import randint, sample, choice
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Giveaway, Lastchecked

# Create your views here.


""" Paginate (divide output by pages) """
def paginate(request, listing): 
    paginator = Paginator(listing, 12)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


""" Populate database using gamepower.com API """
def populate():
    # Get giveaways from gamepower.com
    givs = get('https://www.gamerpower.com/api/giveaways', headers={'Accept': 'application/json'}).json()[::-1]
    # Get recorded giveaway ids from database
    recorded_ids = Giveaway.objects.values_list('gp_id', flat=True)
    for giv in givs:
        # If giveaway already recorded, skip
        if giv['id'] in recorded_ids:
            continue
        else:
            # Set a new giveaway
            title = giv['title']
            image = giv['image']
            description = giv['description']
            instructions = giv['instructions']
            type = giv['type']
            platforms = giv['platforms']
            url = giv['open_giveaway']
            published_date = datetime.strptime(giv['published_date'], '%Y-%m-%d %H:%M:%S')
            gp_id = giv['id']
            # Get all registered users from database
            users = User.objects.values_list('id', flat=True)
            count = users.count()
            # Set giveaway author from registered users randomly
            author = User.objects.get(pk=choice(users))
            # Record new giveaway to database
            new_giv = Giveaway.objects.create(title=title, image=image, description=description, instructions=instructions, type=type, platforms=platforms, url=url, published_date=published_date, gp_id=gp_id, author=author)
            # Set giveaway collectors from registered users randomly
            new_giv.collected.set(sample(list(users), randint(0, count)))
            # Set giveaway worth and expiry_date fields, where available
            if giv['worth'] != 'N/A':
                new_giv.worth = float(giv['worth'].replace('$', ''))
            if giv['end_date'] != 'N/A':
                new_giv.expiry_date = date.fromisoformat(giv['end_date'].split(' ')[0])
            new_giv.save(update_fields=['worth', 'expiry_date'])


def index(request):
    # If database last checked before today, populate (update) it
    if Lastchecked.objects.filter(date__lt=date.today()).exists():
        try:
            populate()
            Lastchecked.objects.first().save()
        except:
            Lastchecked.objects.first().save()
    # Get all giveaways from database
    givs = Giveaway.objects.all()
    # If query parameters set...
    if request.GET.get('by') or request.GET.get('q'):
        #...process query and prepare giveaway list and message
        givs, message = sort_filter(request, givs)
    else:
        #...prepare giveaway list and message
        givs = givs.order_by('-published_date')
        message = f'{givs.count()} Giveaways await your pleasure, {request.user}!'
    # Divide output by pages
    page_obj = paginate(request, givs)
    return render(request, 'grabgamezzz/index.html', {
        'page_obj': page_obj,
        'message': message
    })

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.info(request, 'Invalid username and/or password.')
            return render(request, 'grabgamezzz/login.html', {
                'username': username
            })
    else:
        return render(request, 'grabgamezzz/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        new_user = dict(username=username, first_name=first_name, last_name=last_name, email=email)
        # Ensure password matches confirmation
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            messages.info(request, 'Passwords must match.')
            return render(request, 'grabgamezzz/register.html', {
                'user': new_user
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name'])

        except IntegrityError:
            messages.info(request, 'Username already taken.')
            return render(request, 'grabgamezzz/register.html', {
                'user': new_user
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'grabgamezzz/register.html')


""" Sort and filter giveaways as requested """
def sort_filter(request, givs):
    # Get sort and order parameters, if any
    by = request.GET.get('by', default='published_date')
    order = request.GET.get('order', default='-')
    order_by = order + by
    # Get search query, if any
    q = request.GET.get('q')
    if q:
        givs = givs.filter(title__icontains=q)
        mq = f'for "{q}" query'
    else:
        mq = ''
    # Get filter parameters and filter
    platforms = request.GET.getlist('platforms')
    if platforms:
        givs = givs.filter(reduce(operator.or_, (Q(platforms__icontains=x) for x in platforms)))
    status = request.GET.getlist('status')
    if len(status) == 1:
        today = date.today()
        mstatus = status[0]
        if mstatus == 'expired':
            givs = givs.filter(expiry_date__lt=today)
        else:
            givs = givs.exclude(expiry_date__lt=today)
    else:
        mstatus = ''
    type = request.GET.getlist('type')
    if type:
        givs = givs.filter(reduce(operator.or_, (Q(type__icontains=x) for x in type)))
    givs = givs.order_by(order_by)
    # Make a message on sort, filter and search results
    msorted = {
        'published_date': 'publication date',
        'expiry_date': 'expiry date',
        'worth': 'worthiness',
        'title': 'title'
        }
    morder = {
        '': 'ascending',
        '-': 'descending'
    }
    mtype = f'of {", ".join(type)} {"type" if len(type)==1 else "types"}' if type else ''
    mplatforms = f'for {", ".join(platforms)} {"platform" if len(platforms)==1 else "platforms"}' if platforms else ''
    msort = f'sorted by {msorted[by]} in {morder[order]} order'
    if 'collection' in request.path:
        mcollection = f"in {request.user}'s collection"
    else:
        mcollection = ''
    message = f'Found {givs.count()} {mstatus} {"Giveaway" if givs.count() == 1 else" Giveaways"} {mtype} {mplatforms} {msort} {mq} ' +  mcollection
    return givs, message


def collection(request):
    user = request.user
    # Get all giveaways in user's collection
    collection = Giveaway.objects.filter(collected__username__icontains=user).order_by('-published_date')
    # If query parameters set...
    if request.GET.get('by') or request.GET.get('q'):
        #...process query and prepare giveaway list and message
        collection, message = sort_filter(request, collection)
    else:
        #...prepare giveaway list and message
        message = f'Collection of {collection.count()} {"Giveaway" if collection.count() == 1 else" Giveaways"} selected by {user}'
    # Divide output by pages
    page_obj = paginate(request, collection)
    return render(request, 'grabgamezzz/index.html', {
        'page_obj': page_obj,
        'message': message,
        })

"""Add/remove user to/from giveaway collectors"""
@csrf_exempt
def collect(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        user = request.user
        giv = Giveaway.objects.get(pk=id)
        if user in giv.collected.all():
            giv.collected.remove(user)
        else:
            giv.collected.add(user)
        giv.save()
        count = giv.collected.count()
        return JsonResponse({'count': count})
    else:
        return HttpResponse('Error: Method must be "POST"!')


def profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'GET':
        # Render user's profile page
        return render(request, 'grabgamezzz/profile.html', {
            'user': user,
        })
    else:
        # Find out what to change
        posted_username = request.POST.get('username')
        if posted_username:
            # Change user's data
            user.username = posted_username
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            messages.info(request, 'Your data have been successfully saved!')
        else:
            # Change user's password
            messages.info(request, change_password(request))
        return HttpResponseRedirect(reverse('profile'))


def change_password(request):
    user = User.objects.get(pk=request.user.id)
    old_password = request.POST.get('old_password')
    if not check_password(old_password, user.password):
        return 'Old password is invalid!'
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')
    if new_password1 != new_password2:
        return 'Please verify your new password!'
    user.password = make_password(new_password1)
    user.save()
    #  Update the session with the new password hash
    update_session_auth_hash(request, user)
    return 'Password has been successfully changed!'
        


def submit(request):
    if request.method == 'GET':
        # Render Submit Giveaway page
        return render(request, 'grabgamezzz/submit.html')
    else:
        # Get giveaway form data
        url = request.POST.get('url')
        title = request.POST.get('title')
        image = request.POST.get('image')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        type = request.POST.get('type')
        platforms = request.POST.getlist('platforms')
        platforms =', '.join(platforms)
        worth = request.POST.get('worth')
        expiry_date = request.POST.get('expiry_date')
        # Create a new giveaway
        giv = Giveaway.objects.create(url=url, title=title, image=image, description=description, instructions=instructions, type=type, platforms=platforms, author=request.user)
        # Add optional Worth and Expiry Date data
        if worth:
            giv.worth = float(worth)
        if expiry_date:
            giv.expiry_date = expiry_date
        giv.save(update_fields=['worth', 'expiry_date'])
        messages.info(request, 'New Giveaway has been successfully added!')
        return HttpResponseRedirect(reverse('index'))






