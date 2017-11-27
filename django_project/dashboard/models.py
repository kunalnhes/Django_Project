# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
# create the class which is the table name. variable which are the name of columns.
class User_model(models.Model):
    fullname = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)# adds the current time only once
    updated_on = models.DateTimeField(auto_now=True)    # adds the time whenever data is updated.

class SessionToken(models.Model):
    user_id = models.ForeignKey(User_model)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()

class PostModels(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User_model)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    updated_on = models.DateTimeField(auto_now=True)
    is_liked = models.BooleanField(default=False)

    #django does not allow to acccess this method from html page. We can only access the variables.
    #to use method we need to make this method as proxy variable or virtual variable.
    #although it is method but it behaves as variable in html file
    @property
    def like_count(self):
        return len(LikeModels.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self)

class LikeModels(models.Model):
    user = models.ForeignKey(User_model)
    post = models.ForeignKey(PostModels)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    user = models.ForeignKey(User_model)
    post = models.ForeignKey(PostModels)
    comment_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
