from django.shortcuts import render

from movies.models import Movie

# Create your views here.
def home(request):
    last_added_movies = Movie.objects.all()
    ctx = {'last_added': last_added_movies}
    return render(request, template_name='core/home.html', context=ctx)
