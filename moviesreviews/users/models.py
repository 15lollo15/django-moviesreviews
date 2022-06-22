from email.policy import default
from math import sqrt
from django import views
from django.db import models
from django.shortcuts import get_object_or_404
from moviesreviews.settings import STATIC_URL
from django.core.validators import MaxValueValidator, MinValueValidator
from movies.models import Movie
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    profile_img = models.ImageField(upload_to='imgs/profileImgs/', default=None)
    bio = models.TextField()
    friends = models.ManyToManyField(to='UserProfile', symmetrical=False)
    watch_list = models.ManyToManyField(to=Movie, related_name='in_watchlist')
    is_user_page_public = models.BooleanField(default=True)

    def count_watchlist(self):
        return len(self.watch_list.all())

    def notMyFriends(self):
        return UserProfile.objects.filter(friends = self).exclude(pk__in = self.friends.all())
    
    def count_friends(self):
        return len(self.friends.all())
    
    def count_notMyFriends(self):
        return len(self.notMyFriends())

    def is_editor(self):
        editorGroup = Group.objects.filter(name="Editor").first()
        return editorGroup in self.user.groups.all() or self.user.is_superuser

    def similarity(self, otherProfile):
        movies_in_common = Movie.objects.filter(reviews__in = self.reviews.all()).filter(reviews__in = otherProfile.reviews.all())
        
        if len(movies_in_common) == 0:
            return -1
        
        sum = 0
        my_sqrt_sum = 0
        other_sqrt_sum = 0
        for movie in movies_in_common:
            my_review = Review.objects.filter(owner = self).filter(movie = movie).first()
            other_review = Review.objects.filter(owner = otherProfile).filter(movie = movie).first()
            sum += my_review.rating * other_review.rating

            my_sqrt_sum += my_review.rating * my_review.rating
            other_sqrt_sum += other_review.rating * other_review.rating

        s = sum / (sqrt(my_sqrt_sum) * sqrt(other_sqrt_sum))
        print(str(self) + " " + str(otherProfile) + " " + str(s))
        return s


class Watch(models.Model):
    date = models.DateField()
    user = models.ForeignKey(to='UserProfile', on_delete=models.CASCADE, related_name="watched")
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='views')

class Review(models.Model):
    date = models.DateField()
    owner = models.ForeignKey(to='UserProfile', on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes = models.ManyToManyField(to='UserProfile', related_name="liked_reviews")

    def stars(self):
        return range(self.rating)
    
    def count_likes(self):
        return len(self.likes.all())

class Comment(models.Model):
    date = models.DateField()
    owner = models.ForeignKey(to='UserProfile', on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(to='Review', on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()