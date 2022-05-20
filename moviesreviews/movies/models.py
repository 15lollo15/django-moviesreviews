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

    def stars(self):
        reviews = self.reviews.all()
        if len(reviews) == 0:
            return None
        tot = 0
        for r in reviews:
            tot += r.rating
        return range(int(tot/len(reviews)))
    
    def count_reviews(self):
        return len(self.reviews.all())

    def users_that_reviewed(self):
        users = []
        reviews = self.reviews.all()
        for r in reviews:
            users.append(r.owner)
        return users
    
    def ordered_reviews(self):
        reviews = self.reviews.all()
        return sorted(reviews, key = (lambda r : r.count_likes()), reverse=True)


class Person(models.Model):
    birthday = models.DateField()
    name_surname = models.CharField(max_length=50)

class Genre(models.Model):
    name = models.CharField(max_length=20)