from tabnanny import check
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from network.models import User, Post, Follower, Like
from django import forms
from django.db.models import OuterRef, Subquery, Count, Exists
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core import serializers
import time
import random
import json
from django.core.exceptions import BadRequest
from django.forms.models import model_to_dict
import copy



MAX_POSTS_PER_PAGE = 10


class NewPostForm(forms.Form):
    """The new form class
    """
    post_text = forms.Field(widget=forms.Textarea(
        {'rows': '2','id':'textPost', 'maxlength': 160, 'class': 'form-control', 'placeholder': "What's on your mind?",'style': "resize:none;float:right;padding-top:20px;padding-left:70px;font-size:large;",}), label="New Post", required=True)


class NewEditPostForm(forms.Form):
    """The edit post form class
    """
    id_post_edit_text = forms.Field(widget=forms.Textarea(
        {'rows': '3', 'maxlength': 160, 'class': 'form-control', 'placeholder': "What's happening?", 'id': 'id_post_edit_text'}), label="New Post", required=True)

class EditBio(forms.Form):
    """The edit post form class
    """
    edit_bio = forms.Field(widget=forms.Textarea(
        {'rows': '3', 'maxlength': 160, 'class': 'form-control', 'placeholder': "What's happening?", 'id': 'edit_bio'}), label="New Bio", required=True)
    
def welcome(request):
    usernames = []
    emails = []
    userz = User.objects.all()
    for i in userz:
        usernames.append(i.username)
        emails.append(i.email)
        
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, 'network/welcome.html',context={'TESTING':usernames, 'EMAILS':emails})

def afterLogout(request):
    posts = Post.objects.order_by('-post_date').all()
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for user in posts:
        x = user.user_id
        profile_user = x
        
    total_following = Follower.objects.filter(follower=profile_user).count()
    total_followers = Follower.objects.filter(following=profile_user).count()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "network/afterLogout.html",{
            'total_following': total_following,
            'total_followers': total_followers,
            'posts': page_obj})


def index(request):
    is_following = 0
    if request.user.is_authenticated:
        user = request.session['_auth_user_id']
        username = User.objects.get(id=user)
        likes = Like.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter().order_by(
            '-post_date').annotate(current_like=Count(likes.values('id')))

        
        #List of who the current user follows:
        currentUser = Follower.objects.filter(follower_id=user)

        #Create an empty list with then copy the results
        userFollowing = []
        for i in currentUser:
            userFollowing.append(i.following_id)


        #Create a list for users
        userList=[]

        users = User.objects.all()
        for i in users:
            userList.append(i.id)


        #Create a new List without same elements
        followSuggestions = [x for x in userList if x not in userFollowing]
        suggestionList = []
        for i in followSuggestions:
            x = User.objects.get(id=i)
            suggestionList.append(x)
        
        for i in followSuggestions:
            is_following = Follower.objects.filter(follower=user, following=i).count()

    else:
        posts = Post.objects.order_by('-post_date').all()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {      'username':username,
        'posts': page_obj,
        'form': NewPostForm(),
        'form_edit': NewEditPostForm(),
        'suggestionList': random.sample(suggestionList, 3),
        "is_following": is_following
    })


def following(request):
    if request.user.is_authenticated:
        user = request.session['_auth_user_id']
        followers = Follower.objects.filter(follower=user)
        likes = Like.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter(user_id__in=followers.values('following_id')).order_by(
            '-post_date').annotate(current_like=Count(likes.values('id')))
    else:
        return HttpResponseRedirect(reverse("login"))

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        'posts': page_obj,
        'form': NewPostForm()
    })


def postmessage(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.session['_auth_user_id'])
            text = form.cleaned_data["post_text"]
            post = Post(user=user, text=text)
            post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def editpost(request, id):
    if request.is_ajax and request.method == "POST":
        form = NewEditPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["id_post_edit_text"]
            Post.objects.filter(
                id=id, user_id=request.session['_auth_user_id']).update(text=text)
            return JsonResponse({"result": 'ok', 'text': text})
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": HttpResponseBadRequest("Bad Request: no like chosen")}, status=400)



def editbio(request, id):
    if request.is_ajax and request.method == "POST":
        form = EditBio(request.POST)
        if form.is_valid():
            text = form.cleaned_data["edit_bio"]
            Post.objects.filter(
                id=id, user_id=request.session['_auth_user_id']).update(text=text)
            return JsonResponse({"result": 'ok', 'text': text})
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": HttpResponseBadRequest("Bad Request: no like chosen")}, status=400)


def follow(request, id):
    try:
        result = 'follow'
        user = User.objects.get(id=request.session['_auth_user_id'])
        user_follower = User.objects.get(id=id)
        follower = Follower.objects.get_or_create(
            follower=user, following=user_follower)
        
        followinguser = str(user_follower)
        user_profile = str(user_follower.profile_image.url)
        bio = str(user_follower.bio)
        
        if not follower[1]:
            Follower.objects.filter(follower=user, following=user_follower).delete()
            result = 'unfollow'
        total_followers = Follower.objects.filter(following=user_follower).count()

    except KeyError:
        return HttpResponseBadRequest("Bad Request: no like chosen")
    return JsonResponse({"result": result, "total_followers": total_followers, "followinguser": followinguser, "user_profile": user_profile,"bio":bio})


def like(request, id):

    try:
        css_class = 'fas fa-heart'
        user = User.objects.get(id=request.session['_auth_user_id'])
        post = Post.objects.get(id=id)
        like = Like.objects.get_or_create(
            user=user, post=post)
        if not like[1]:
            css_class = 'far fa-heart'
            Like.objects.filter(user=user, post=post).delete()

        total_likes = Like.objects.filter(post=post).count()
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no like chosen")
    return JsonResponse({
        "like": id, "css_class": css_class, "total_likes": total_likes
    })


def profile(request, username):
    is_following=0
    profile_user = User.objects.get(username=username)
    # Saving a QuerySet of User's Following
    followingList = Follower.objects.filter(follower=int(profile_user.id))
    # Saving a QuerySet of User's Followers
    followersList = Follower.objects.filter(following=int(profile_user.id))
    
    if request.user.is_authenticated:
        logged_user = request.session['_auth_user_id']
        followers = Follower.objects.filter(follower=logged_user)
        username = User.objects.get(id=logged_user)
        is_followingg = Follower.objects.filter(
        follower=logged_user, following=profile_user.id).count()

        likes = Like.objects.filter(post=OuterRef('id'), user_id=logged_user)
        posts = Post.objects.filter(user=profile_user).order_by(
            'post_date').annotate(current_like=Count(likes.values('id')))
        
        
        #List of who the current user follows:
        currentUser = Follower.objects.filter(follower_id=logged_user)

        #Create an empty list with then copy the results
        userFollowing = []
        for i in currentUser:
            userFollowing.append(i.following_id)


        #Create a list for users
        userList=[]

        users = User.objects.all()
        for i in users:
            userList.append(i.id)


        #Create a new List without same elements
        followSuggestions = [x for x in userList if x not in userFollowing]
        suggestionList = []
        for i in followSuggestions:
            x = User.objects.get(id=i)
            suggestionList.append(x)
        
        for i in followSuggestions:
            is_following = Follower.objects.filter(follower=logged_user, following=i).count()
    else:
        posts = Post.objects.filter(
            user=profile_user).order_by('post_date').all()


    total_following = Follower.objects.filter(
        follower=profile_user).count()
    total_followers = Follower.objects.filter(
        following=profile_user).count()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    tmpJson = serializers.serialize("json",followingList)
    tmpObj = json.loads(tmpJson)
    

    
    return render(request, "network/profile.html", { "followersList": followersList,
    "followingList": followingList,
    "userinfo": json.dumps(tmpObj),
     "user_profile": profile_user, 
     "posts": page_obj, 
     "is_following": is_followingg, 
     'total_following': total_following, 
     'total_followers': total_followers,
     "username":username,
     'suggestionList': random.sample(suggestionList, 3),
     'form': NewPostForm(), 'form_edit': NewEditPostForm(),
     
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
            return render(request, "network/welcome.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("afterLogout"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        profile_image = request.FILES['image']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profile_image=profile_image,cover_image='/images/mars.jpg')
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



# Testing
def notifications(request):
    is_following = 0
    if request.user.is_authenticated:
        user = request.session['_auth_user_id']
        username = User.objects.get(id=user)
        followingList = Follower.objects.filter(follower=int(user))
        # Saving a QuerySet of User's Followers
        followersList = Follower.objects.filter(following=int(user))
        
        tmpJson = serializers.serialize("json",followersList)
        tmpObj = json.loads(tmpJson)
        x = json.dumps(tmpObj)
        likes = Like.objects.filter(post=OuterRef('id'), user_id=user)
        posts = Post.objects.filter().order_by(
            '-post_date').annotate(current_like=Count(likes.values('id')))
        
        '''
        '''
        #List of who the current user follows:
        currentUser = Follower.objects.filter(follower_id=user)

        #Create an empty list with then copy the results
        userFollowing = []
        for i in currentUser:
            userFollowing.append(i.following_id)


        #Create a list for users
        userList=[]

        users = User.objects.all()
        for i in users:
            userList.append(i.id)


        #Create a new List without same elements
        followSuggestions = [x for x in userList if x not in userFollowing]
        suggestionList = []
        for i in followSuggestions:
            x = User.objects.get(id=i)
            suggestionList.append(x)
        
        for i in followSuggestions:
            is_following = Follower.objects.filter(follower=user, following=i).count()
    else:
        posts = Post.objects.order_by('-post_date').all()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/notifications.html", {
        "username":username,
        'posts': page_obj,
        'form': NewPostForm(),
        'form_edit': NewEditPostForm(),
        "followingList": followingList,
        "followersList":followersList,
        "xx":json.dumps(tmpObj),
        ###
        'suggestionList': random.sample(suggestionList, 3),
        "is_following": is_following
        ###
    })
    
    
def updateInfo(request):
    if request.user.is_authenticated:
        id = request.session['_auth_user_id']
        updateUser = User.objects.get(id=id)
        
        newCover = request.FILES['cover'] if 'cover' in request.FILES else False
        newImage = request.FILES['image'] if 'image' in request.FILES else False
        
        newBio = request.POST["bio"]
        
        if newBio:
            updateUser.bio = newBio
            updateUser.save()
        else:
            pass
        
        if newCover:
            updateUser.cover_image = newCover
            updateUser.save()
        else:
            pass
        
        if newImage:
            updateUser.profile_image = newImage
            updateUser.save()
        else:
            pass


    return HttpResponseRedirect(reverse("profile", args=(updateUser.username,)))


# Testing for AJAX
def testing(request):
    usernames = []
    userz = User.objects.all()
    for i in userz:
        usernames.append(i.username)
    

    return render(request, 'network/testing.html',{'FOLLOWERZ':usernames})

'''
def jsonresponse2(request, username):
    profile_user = User.objects.get(username=username)
    followingList = Follower.objects.filter(follower=int(profile_user.id))
    

    
    following = []
    for i in followingList:
        user = i.following.profile_image.url
        following.append(user)
    
        
    followingJSON = serializers.serialize('json', following)
    
    
    
    dict_obj = model_to_dict(followingList)
    
    return HttpResponse(followingJSON, content_type='application/json')
'''
'''
def jsonresponseExample(request, username):
    Current_User = User.objects.get(username=username)
    #List of who this user follows
    followingList = Follower.objects.filter(follower=int(Current_User.id))
    
    UserInfoList = []
    for user in followingList:
        singleUser = User.objects.filter(username=user.following).values( 'username','bio', 'profile_image')
        UserInfoList.append(singleUser)
    
    
    results = Follower.objects.filter(follower=int(Current_User.id)).values('follower', 'following', 'following_id')
    results2 = User.objects.filter(username='mn').values( 'username','bio', 'profile_image')
    
    return JsonResponse({'results':list(results), 'results2':list(results2)})
    
'''



def jsonresponse(request, username):
    if request.method == 'GET':
        username = request.session['_auth_user_id']
        
        Current_User = User.objects.get(id=username)
        
        #List of who this user follows
        followingList = Follower.objects.filter(follower=int(Current_User.id))
            
        UsersInfo = []
        
        for user in followingList:
            singleUser = User.objects.filter(username=user.following).values( 'username','bio', 'profile_image','id')
            UsersInfo += singleUser
    else:
        return JsonResponse({'Error':'Method Not Allowed!'})
    return JsonResponse({'UsersInfo':list(UsersInfo)})
    
    
def allUsers(request):
    if request.method == 'GET' or "POST":
        users = []
        user = ''
        allUsers = User.objects.all().values('username')
        for i in allUsers:
            user = copy.copy(i['username'])
            users.append(user)
    

    return JsonResponse({'UsersInfo':list(users)})

def mobile(request):
    if request.user.is_authenticated:

        return render(request, "network/mobile.html")



##################################
##################################
def jsonresponse2(request, username):
    if request.method == 'GET' and request.user.is_authenticated:
        username = request.session['_auth_user_id']
        
        Current_User = User.objects.get(id=username)
        
        #List of who this user follows
        followingList = Follower.objects.filter(follower=int(Current_User.id))
            
        UsersInfo = []
        
        
        #Create a list for users
        userList=[]

        users = User.objects.all()
        for i in users:
            userList.append(i.id)


        #Create a new List without same elements
        followSuggestions = [x for x in userList if x not in followingList]
        
        suggestionList = []
        for i in followSuggestions:
            x = User.objects.filter(id=i).values('id','username','bio','profile_image')
            suggestionList += x
            
        
        for user in followingList:
            singleUser = User.objects.filter(username=user.following).values( 'username','bio', 'profile_image','id')
            UsersInfo += singleUser
            
    else:
        return JsonResponse({'Error':'Method Not Allowed!'})
    return JsonResponse({'suggestions':list(suggestionList)})
