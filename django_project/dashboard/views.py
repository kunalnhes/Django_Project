# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from forms import SignUp_form, Login_form, Like_form, Comment_form, Post_form
from django.contrib.auth.hashers import  make_password,check_password
from models import User_model,SessionToken, PostModels,LikeModels,CommentModel
from imgurpython import ImgurClient
from django_project.settings import BASE_DIR, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET
import os

# Create your views here.

def signup_view(request):
    now_time=datetime.now()
    if request.method == "GET":
        form = SignUp_form()
        #We created a object of Django mapper form and passed this to the htmlfile in the dictionary with key form
        return render(request,'SignUp.html',{'now':now_time, 'form':form})
    else:
        #request is Post. Process form data
        #request contains the filled form which is returned by form
        #request.POST contains all the post data. Django captures all the data and stores it in the form
        form= SignUp_form(request.POST)
        if form.is_valid():
            #form.isvalid() this method tells wether the form object data is valid or not.
            #read data from form objects
            #the key inside cleaned data will be the name of the input field in html
            fullname = form.cleaned_data['fullname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            #encrypt the password

            password = make_password(password)

            #save data to database

            user = User_model(fullname=fullname, username=username, password=password,email=email)
            user.save()
            return render(request,'Success.html')

def login_view(request):
    if request.method == 'GET':
        lform = Login_form()
        return render(request,'Login.html',{'login_form':lform})
    else:
        lform = Login_form(request.POST)
        if lform.is_valid():
            error_msg = ""
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']

            #read data from database
            user=User_model.objects.filter(username=username).first()
            if user:
                #compare Password
                if check_password(password,user.password):
                    #login Successful. redirect to feed page
                    #create session token
                    token = SessionToken(user_id=user)
                    token.create_token()
                    print token.session_token
                    token.save()

                    #redirect to feed
                    #there is redirect method in Django which takes the page to different url
                    response = redirect('/feed/')
                    #inside response object there is default method set cookie.
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    #password not matched
                    error_msg = "Wrong Password. LOL!!"
                    return render(request,"Login.html",{'error_msg':error_msg})
            else:
                error_msg = "Wrong Username ROFL!!!!"
                return render(request,"Login.html",{'error_msg': error_msg})

def logout_view(request):
    response = redirect("/")
    response.delete_cookie("session_token")
    return response

def home_view(request):
    return render(request,'Home.html')

def feed_view(request):
    user = check_validation(request)
    if user:
        #user already login
        posts=PostModels.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModels.objects.filter(post=post, user=user).first()
            if existing_like:
                #post is already liked
                post.is_liked = True

        return render(request,'Feed.html',{'all_posts':posts})
    else:
        return redirect("/login/")

def like_view(request):
    user = check_validation(request)
    if user:
        #user is logged in
        if request.method == 'GET':
            return redirect('/feed/')
        else:
            #form is submitted
            like_form = Like_form(request.POST)
            if like_form.is_valid():
                post_id = like_form.cleaned_data.get('post')

                existing_like = LikeModels.objects.filter(post=post_id,user=user).first()
                #when only we need to check if value exists or not we use .exists()with the result of database
                if not existing_like:
                    #post is not liked
                    LikeModels.objects.create(post=post_id, user=user)#this is a new way to save data without using save method
                else:
                    #post is already liked
                    existing_like.delete()
                return redirect("/feed/")
            else:
                return HttpResponse("Form Data is invalid")
    else:
        return redirect("/login/")

def comment_view(request):
    user = check_validation(request)
    if user:
        #user already loged in
        if request.method == 'POST':
            comment_form = Comment_form(request.POST)
            if comment_form.is_valid():
                post_id = comment_form.cleaned_data.get('post')
                comment_text = comment_form.cleaned_data.get('comment_text')


                #save this data in Database
                CommentModel.objects.create(post=post_id,user=user,comment_text=comment_text)
                return redirect("/feed/")

        else:
            pass
    else:
        #user not loged in
        return redirect("/login/")

def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'GET':
            form = Post_form()
            return render(request, 'post.html', {'post_form':form})
        else:
            #post data
            form = Post_form(request.POST,request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                new_post = PostModels(user=user,image=image,caption=caption)
                new_post.save()

                path = os.path.join(BASE_DIR,new_post.image.url)
                client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
                new_post.image_url = client.upload_from_path(path,anon=True)['link']
                new_post.save()
                return HttpResponse("Image saved")
    else:
        return redirect("/login/")

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user_id
        else:
            return None
