from django.utils import timezone
from sqlite3 import Date, Time
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput, ModelForm, TextInput, Select
from movies.models import Movie


from users.models import Comment, Review

@login_required
def like(request):
    review_pk = request.GET['reviewpk']
    user = get_object_or_404(User, username=request.user)
    review = get_object_or_404(Review, pk = review_pk)

    r_text = "like"
    if user.profile in review.likes.all():
        review.likes.remove(user.profile)
        r_text = "not_like"
    else:
        review.likes.add(user.profile)
    r_text += "," + str(len(review.likes.all()))

    return HttpResponse(r_text)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'rating']
        widgets = {
            'rating' : Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
        }

@login_required
def newReview(request):
    user = get_object_or_404(User, username=request.user)
    form = ReviewForm(request.POST)
    if (form.is_valid()):
        moviePK = request.POST.get("movie-pk")
        movie = get_object_or_404(Movie, pk = moviePK)
        if len(Review.objects.filter(owner = user.profile, movie = movie)) > 0:
            pass
        else:
            review = Review()
            review.owner = user.profile
            review.movie = movie
            review.rating = int(form.cleaned_data['rating'])
            review.date = timezone.now()
            review.body = form.cleaned_data['body']
            review.save()
        print(moviePK)
    return HttpResponse("ok")