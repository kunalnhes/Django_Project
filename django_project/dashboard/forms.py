from django import forms
from models import User_model,LikeModels,CommentModel,PostModels
#to connect with database we inherits ModelForm
#we provide meta information about the class. just like inner class. the name must be Meta.
#this Meta class contains only two values model and field
#model: Which database table must map with the form
#fields: will be a list which all columns shall we need to map.
class SignUp_form(forms.ModelForm):
    class Meta:
        model = User_model
        fields = ['fullname','username','email','password']

class Login_form(forms.ModelForm):
    class Meta:
        model = User_model
        fields = ['username','password']

class Like_form(forms.ModelForm):
    class Meta:
        model = LikeModels
        fields = ['post']

class Comment_form(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['post','comment_text']

class Post_form(forms.ModelForm):
    class Meta:
        model = PostModels
        fields = ['image','caption']