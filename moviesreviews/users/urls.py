from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views


from users.views import *

app_name = 'users'

urlpatterns = [
    path('like/', like, name="like"),
    path('newcomment/', new_comment, name="new_comment"),
    path('deletecomment/', delete_comment, name="delete_comment"),
    path('newreview/', new_review, name="new_review"),
    path('deletereview/', delete_review, name="delete_review"),
    path('details/<pk>/', ProfileDetails.as_view(), name="profile_details"),
    path('addtowatchlist/', add_to_watchlist, name="addtowatchlist"),
    path('removefromwatchlist/', remove_from_watchlist, name="removefromwatchlist"),
    path('addremovefriend/', add_remove_friend, name="addremovefriend"),
    path('addwatch/', add_watch, name="addwatch"),
    path('friends/<pk>/', FriendsPage.as_view(), name="friends"),
    path('updateProfile', UpdateUserProfile.as_view(), name="updateprofile"),
    path('search/', SearchProfile.as_view(), name="search_profile"),
    path('upgradedowngrade/', upgrade_or_downgrade, name="upgradedowngrade")
]
