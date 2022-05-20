from django.shortcuts import render
from django.views.generic.detail import DetailView

from movies.models import Movie
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

    