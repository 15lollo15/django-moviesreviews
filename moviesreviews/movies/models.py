from datetime import timedelta
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    added_date = models.DateField()
    release_year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    duration = models.PositiveSmallIntegerField()  # In minutes
    directors = models.ManyToManyField(to='Person', related_name='movies_as_director')
    cast = models.ManyToManyField(to='Person', related_name='movies_as_actor')
    plot = models.TextField()
    genre = models.ManyToManyField(to='Genre', related_name='movies')
    cover = models.ImageField(upload_to='imgs/covers/', default=None)

    def score_by(self, user):
        review = self.reviews.filter(owner=user).first()
        if review is None:
            return 0
        return review.rating

    def count_recent_views(self):
        days_ago = timezone.now() - timedelta(days=30)
        n = len(self.views.filter(date__gt=days_ago))
        return n

    def stars(self):
        reviews = self.reviews.all()
        if len(reviews) == 0:
            return []
        tot = 0
        for r in reviews:
            tot += r.rating
        return range(int(tot / len(reviews)))

    def users_that_reviewed(self):
        users = []
        reviews = self.reviews.all()
        for r in reviews:
            users.append(r.owner)
        return users

    def ordered_reviews(self):
        reviews = self.reviews.all()
        return sorted(reviews, key=(lambda r: len(r.likes.all())), reverse=True)


class Person(models.Model):
    birthday = models.DateField()
    name_surname = models.CharField(max_length=50)

    def is_a_director(self):
        return len(self.movies_as_director.all()) > 0

    def is_an_actor(self):
        return len(self.movies_as_actor.all()) > 0

    def __str__(self):
        return self.name_surname + " (" + str(self.birthday) + ")"


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
