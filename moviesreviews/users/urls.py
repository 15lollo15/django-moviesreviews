from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from movies.views import *
from users.views import like, newReview

app_name = 'users'

urlpatterns = [
    path('like/', like, name="like"),
    path('newreview/', newReview, name="new_review")
]
