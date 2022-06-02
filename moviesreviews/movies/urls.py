from django.urls import path

from movies.views import *

app_name = 'movies'

urlpatterns = [
    path('details/<pk>/', MovieDetails.as_view(), name="moviedetails"),
    path('search/', SearchView.as_view(), name="searchmovie"),
    path('updatemovie/<pk>/', UpdateMovie.as_view(), name="updatemovie"),
    path('deletemovie/<pk>/', DeleteMovie.as_view(), name="deletemovie"),
    path('createmovie/', CreateMovie.as_view(), name="createmovie")
]