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
        context["is_in_user_watchlist"] = False


        movie = context["object"]

        if self.request.user.is_authenticated:
            context["is_in_user_watchlist"] = self.request.user.profile in movie.in_watchlist.all()

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

        movies = movies.order_by("title")

        order_r = self.request.GET.get('order-by', None)
        if order_r == "title-desc":
            movies = movies.order_by("-title")
        elif order_r == "year-asc":
            movies = movies.order_by("release_year")
        elif order_r == "year-desc":
            movies = movies.order_by("-release_year")
        elif order_r == "rating-asc":
            movies = sorted(movies, key=(lambda m : m.count_stars()))
        elif order_r == "rating-desc":
            movies = sorted(movies, key=(lambda m : m.count_stars()), reverse=True)
        elif order_r == "last-added":
            movies = movies.order_by("added_date")
        elif order_r == "trand":
            #TODO
            pass

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

        order_by = self.request.GET.get("order-by")
        context["selected_order"] = order_by

        context["title"] = self.request.GET.get('title', "")
        return context
    

