from django.db import models

class Movie(models.Model):
    release_year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    director = models.ManyToManyField(to='Person', related_name='movies_as_director')
    cast = models.ManyToManyField(to='Person', related_name='movies_as_actor')
    plot = models.TextField()
    genre = models.ManyToManyField(to='Genre', related_name='movies')
    cover_path = models.URLField()


class Person(models.Model):
    name = models.CharField(max_length=20)
    surame = models.CharField(max_length=20)

class Genre(models.Model):
    name = models.CharField(max_length=20)