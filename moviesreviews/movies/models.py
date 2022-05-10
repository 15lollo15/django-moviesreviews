from django.db import models

class Movie(models.Model):
    added_date = models.DateField()
    release_year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    directors = models.ManyToManyField(to='Person', related_name='movies_as_director')
    cast = models.ManyToManyField(to='Person', related_name='movies_as_actor')
    plot = models.TextField()
    genre = models.ManyToManyField(to='Genre', related_name='movies')
    cover_path = models.URLField()


class Person(models.Model):
    birthday = models.DateField()
    name_surname = models.CharField(max_length=50)

class Genre(models.Model):
    name = models.CharField(max_length=20)