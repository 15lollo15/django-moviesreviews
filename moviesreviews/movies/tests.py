from django.utils import timezone
from django.test import TestCase

from movies.models import Genre, Movie, Person

# Create your tests here.
class PersonTest(TestCase):
    def test_is_an_actor_with_no_movies_as_actor(self):
        non_actor = Person(birthday = timezone.now(), name_surname = "Mario Rossi")
        non_actor.save()
        self.assertFalse(non_actor.is_an_actor())
    
    def test_is_an_actor_with_a_movie_as_actor(self):
        genre = Genre(name = "Giallo")
        genre.save()
        director = Person(birthday = timezone.now(), name_surname = "Luigi Verdi")
        director.save()
        actor = Person(birthday = timezone.now(), name_surname = "Mario Rossi")
        actor.save()
        movie = Movie(added_date = timezone.now(), 
                    release_year = "2000", 
                    title = "test", 
                    duration = "90",
                    plot = "test plot" 
                    )
        movie.save()
        movie.directors.set([director])
        movie.cast.set([actor])
        movie.genre.set([genre])
        movie.save()
        self.assertTrue(actor.is_an_actor())

    def test_is_a_director_with_no_movies_as_director(self):
        non_director = Person(birthday = timezone.now(), name_surname = "Mario Rossi")
        non_director.save()
        self.assertFalse(non_director.is_a_director())
    
    def test_is_a_actor_with_a_movie_as_director(self):
        genre = Genre(name = "Giallo")
        genre.save()
        director = Person(birthday = timezone.now(), name_surname = "Luigi Verdi")
        director.save()
        actor = Person(birthday = timezone.now(), name_surname = "Mario Rossi")
        actor.save()
        movie = Movie(added_date = timezone.now(), 
                    release_year = "2000", 
                    title = "test", 
                    duration = "90",
                    plot = "test plot" 
                    )
        movie.save()
        movie.directors.set([director])
        movie.cast.set([actor])
        movie.genre.set([genre])
        movie.save()
        self.assertTrue(director.is_a_director())