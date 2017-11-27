"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from dashboard.views import signup_view,login_view,home_view,feed_view
from dashboard import views
urlpatterns = [
    url(r'^signup/$',views.signup_view,name='signup'),
    url(r'^feed/$',views.feed_view,name='feed'),
    url(r'^$',views.home_view,name='home'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^like/$', views.like_view, name='like'),
    url(r'^post/$', views.post_view, name='post'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^comment/$', views.comment_view, name='comment'),
    url(r'^admin/', admin.site.urls),
]
