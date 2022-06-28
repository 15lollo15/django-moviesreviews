from django.urls import path

from movies.views import MovieDetails, CreatePerson, CreateGenre, SearchMovie, UpdateMovie, DeleteMovie, CreateMovie

app_name = 'movies'

urlpatterns = [
    path('details/<pk>/', MovieDetails.as_view(), name="moviedetails"),
    path('createperson/', CreatePerson.as_view(), name="createperson"),
    path('creategenre/', CreateGenre.as_view(), name="creategenre"),
    path('search/', SearchMovie.as_view(), name="searchmovie"),
    path('updatemovie/<pk>/', UpdateMovie.as_view(), name="updatemovie"),
    path('deletemovie/<pk>/', DeleteMovie.as_view(), name="deletemovie"),
    path('createmovie/', CreateMovie.as_view(), name="createmovie")
]