from django.urls import path

from movies.views import *

app_name = 'movies'

urlpatterns = [
    path('details/<pk>/', MovieDetails.as_view(), name="moviedetails")
]