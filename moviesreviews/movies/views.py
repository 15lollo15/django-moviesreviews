from django.shortcuts import render
from django.views.generic.detail import DetailView

from movies.models import Movie

# Create your views here.
class MovieDetails(DetailView):
    model = Movie
    template_name = 'movies/movieDetails.html'