from django.db import models
from moviesreviews.settings import STATIC_URL
from django.core.validators import MaxValueValidator, MinValueValidator
from movies.models import Movie
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    profile_img_path = models.URLField(default=('imgs/profiles_imgs/default.jpg'))
    bio = models.TextField()
    friends = models.ManyToManyField(to='UserProfile', symmetrical=False)
    watch_list = models.ManyToManyField(to=Movie, related_name='in_watchlist')
    is_user_page_public = models.BooleanField(default=True)

    def notMyFriends(self):
        return UserProfile.objects.filter(friends = self).exclude(pk__in = self.friends.all())
    
    def count_friends(self):
        return len(self.friends.all())
    
    def count_notMyFriends(self):
        return len(self.notMyFriends())


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