from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from movies.views import *
from users.views import ProfileDetails, addToWatchlist, deleteReview, like, newReview

app_name = 'users'

urlpatterns = [
    path('like/', like, name="like"),
    path('newreview/', newReview, name="new_review"),
    path('deletereview/', deleteReview, name="delete_review"),
    path('details/<pk>/', ProfileDetails.as_view(), name="profile_details"),
    path('addtowatchlist/', addToWatchlist, name="addtowatchlist")
]
