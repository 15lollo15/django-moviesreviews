from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from movies.views import *
from users.views import ProfileDetails, addRemoveFriend, addToWatchlist, deleteReview, like, newReview, removeFromWatchlist

app_name = 'users'

urlpatterns = [
    path('like/', like, name="like"),
    path('newreview/', newReview, name="new_review"),
    path('deletereview/', deleteReview, name="delete_review"),
    path('details/<pk>/', ProfileDetails.as_view(), name="profile_details"),
    path('addtowatchlist/', addToWatchlist, name="addtowatchlist"),
    path('removefromwatchlist/', removeFromWatchlist, name="removefromwatchlist"),
    path('addremovefriend/', addRemoveFriend, name="addremovefriend")
]
