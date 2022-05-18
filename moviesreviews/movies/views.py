from django.shortcuts import render
from django.views.generic.detail import DetailView

from movies.models import Movie
from users.views import ReviewForm

class MovieDetails(DetailView):
    model = Movie
    template_name = 'movies/movieDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context
    