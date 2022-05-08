from movies.models import Genre, Movie, Person

def erase_db():
    print("Erase the DB")
    Movie.objects.all().delete()
    Person.objects.all().delete()
    Genre.objects.all().delete()

def init_db():
    print("Init the DB")
    if len(Movie.objects.all()) != 0 or len(Person.objects.all()) != 0 or len(Genre.objects.all()) != 0:
        return
    
    genre_list = ['horror', 'fantasy', 'family', 'crime', 'animation']
    for g_name in genre_list:
        genre = Genre()
        genre.name = g_name
        genre.save()