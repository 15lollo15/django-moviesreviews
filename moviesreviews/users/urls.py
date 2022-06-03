from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from movies.views import *
from users.views import *

app_name = 'users'

urlpatterns = [
    path('like/', like, name="like"),
    path('newreview/', newReview, name="new_review"),
    path('deletereview/', deleteReview, name="delete_review"),
    path('details/<pk>/', ProfileDetails.as_view(), name="profile_details"),
    path('addtowatchlist/', addToWatchlist, name="addtowatchlist"),
    path('removefromwatchlist/', removeFromWatchlist, name="removefromwatchlist"),
    path('addremovefriend/', addRemoveFriend, name="addremovefriend"),
    path('addwatch/', addWatch, name="addwatch"),
    path('friends/<pk>/', FriendsPage.as_view(), name="friends"),
    path('updateProfile', UpdateUserProfile.as_view(), name="updateprofile"),
    path('search/', SearchProfile.as_view(), name="search_profile"),
    path('upgradedowngrade/', updateOrDowngrade, name="upgradedowngrade")
]
