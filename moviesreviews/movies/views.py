from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from movies.models import Genre, Movie
from users.models import Review
from users.views import ReviewForm

class MovieDetails(DetailView):
    model = Movie
    template_name = 'movies/movieDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        context["user_review"] = None

        movie = context["object"]
        reviews = movie.ordered_reviews()
        if self.request.user.is_authenticated:
            rs = Review.objects.filter(owner = self.request.user.profile, movie = movie)
            if len(rs) > 0:
                reviews.remove(rs.first())
                reviews.insert(0, rs.first())
                context["user_review"] = rs.first()

        context["reviews"] = reviews
        return context

class SearchView(ListView):
    model = Movie
    template_name = 'movies/search.html'

    def get_queryset(self):
        movies = Movie.objects.all()
        title = self.request.GET.get('title', None)
        if title != None:
            movies = movies.filter(title__icontains = title)
        genre_r = self.request.GET.get('genre', None)
        if genre_r != None and genre_r != "":
            genre = Genre.objects.filter(name=genre_r)
            movies = movies.filter(genre__in= genre)
        return movies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["selected_genre"] = self.request.GET.get('genre', '')
        context["title"] = self.request.GET.get('title', "")
        return context
    

    