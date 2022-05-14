from django.shortcuts import render

from movies.models import Movie

# Create your views here.
def home(request):
    last_added_movies = Movie.objects.order_by('-added_date')[:4]
    trend_movies = Movie.objects.all()[:4]
    ctx = {'last_added' : last_added_movies, 'trend_movies' : trend_movies}
    return render(request, template_name='core/home.html', context=ctx)
