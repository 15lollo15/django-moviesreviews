from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from movies.models import Genre, Movie, Person
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
            genre = Genre.objects.filter(pk=genre_r)
            movies = movies.filter(genre__in= genre)

        directors_r = self.request.GET.get('director', None)
        if directors_r != None and directors_r != "":
            directors = Person.objects.filter(pk=directors_r)
            movies = movies.filter(directors__in= directors)
        
        actors_r = self.request.GET.get('actor', None)
        if actors_r != None and actors_r != "":
            actors = Person.objects.filter(pk=actors_r)
            movies = movies.filter(cast__in= actors)

        return movies
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["people"] = Person.objects.all()
        genre = self.request.GET.get('genre', 0)
        if genre == "":
            genre = 0
        context["selected_genre"] = int(genre)

        director = self.request.GET.get('director', 0)
        if director == "":
            director = 0
        context["selected_director"] = int(director)

        actor = self.request.GET.get('actor', 0)
        if actor == "":
            actor = 0
        context["selected_actor"] = int(actor)

        context["title"] = self.request.GET.get('title', "")
        return context
    

    