import django
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from sqlite3 import Date, Time
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput, ModelForm, TextInput, Select
from django.views.generic.detail import DetailView
from movies.models import Genre, Movie
from django.db.models import Count, Sum
import datetime


from users.models import Comment, Review, UserProfile, Watch

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
        reviews = Review.objects.filter(owner = user.profile, movie = movie)
        if len(reviews) > 0:
            r = reviews.first()
            r.date = timezone.now()
            r.body = form.cleaned_data['body']
            r.rating = int(form.cleaned_data['rating'])
            r.save()
        else:
            review = Review()
            review.owner = user.profile
            review.movie = movie
            review.rating = int(form.cleaned_data['rating'])
            review.date = timezone.now()
            review.body = form.cleaned_data['body']
            review.save()
    return redirect(reverse('movies:moviedetails', args=[moviePK]))

@login_required
def addToWatchlist(request):
    user = get_object_or_404(User, username=request.user)
    moviePK = request.GET.get("movie-pk")
    movie = get_object_or_404(Movie, pk = moviePK)
    r_text = "added"
    if movie in user.profile.watch_list.all():
        user.profile.watch_list.remove(movie)
        r_text = "removed"
    else:
        user.profile.watch_list.add(movie)

    return HttpResponse(r_text)

@login_required
def deleteReview(request):
    user = get_object_or_404(User, username=request.user)
    moviePK = request.POST.get("movie-pk")
    movie = get_object_or_404(Movie, pk = moviePK)
    review = get_object_or_404(Review, owner = user.profile, movie = movie)
    review.delete()
    return redirect(reverse('movies:moviedetails', args=[moviePK]))

@login_required
def removeFromWatchlist(request):
    user = get_object_or_404(User, username=request.user)
    moviePK = request.POST.get("movie-pk")
    movie = get_object_or_404(Movie, pk = moviePK)
    is_viewed = request.POST.get("is-viewed", None)
    if is_viewed == None:
        is_viewed = False
    else:
        is_viewed = (is_viewed == "True")
    user.profile.watch_list.remove(movie)

    if is_viewed:
        watch = Watch()
        watch.movie = movie
        watch.user = user.profile
        watch.date = timezone.now()
        watch.save()
    
    return redirect(reverse('users:profile_details', args=[user.profile.pk]))

@login_required
def addRemoveFriend(request):
    myUser = get_object_or_404(User, pk = request.user.pk)
    myProfile = get_object_or_404(UserProfile, user = myUser)

    otherProfile = get_object_or_404(UserProfile, pk = request.POST.get('profile-pk', None))

    if myProfile == otherProfile:
        return redirect(reverse('users:profile_details', args=[otherProfile.pk]))

    if otherProfile in myProfile.friends.all():
        myProfile.friends.remove(otherProfile)
    else:
        myProfile.friends.add(otherProfile)

    return redirect(reverse('users:profile_details', args=[otherProfile.pk]))


class ProfileDetails(LoginRequiredMixin,DetailView):
    model = UserProfile
    template_name = 'users/profileDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profileOwner = context["object"]
        context['can_show'] = True
        context['favourite_movie'] = None
        context['favourite_genre'] = None
        context['watchtime'] = None

        # Favourite movie
        watches = Watch.objects.filter(user=profileOwner).values("movie").annotate(mcount = Count("movie")).order_by("-mcount")
        if len(watches.all()) > 0:
            w = watches.all().first()
            context['favourite_movie'] = get_object_or_404(Movie, pk = w["movie"])

        # Favourite genre
        watches = Watch.objects.filter(user=profileOwner).values("movie")
        movies = Movie.objects.filter(pk__in = watches).values("genre").annotate(gcount = Count("genre")).order_by("-gcount")
        if len(movies.all()) > 0:
            m = movies.all().first()
            context['favourite_genre'] = get_object_or_404(Genre, pk = m["genre"])
        
        
        # Watch time
        watches = Watch.objects.filter(user=profileOwner).filter(date__gt = (timezone.now() - datetime.timedelta(days=30))).values("movie")
        movies = Movie.objects.filter(pk__in = watches).aggregate(Sum('duration'))
        if len(movies) > 0:
            context['watchtime'] = movies["duration__sum"]
        

        if profileOwner.is_user_page_public:
            return context

        user = get_object_or_404(User, pk = self.request.user.pk)
        profile = get_object_or_404(UserProfile, user = user)

        if profile not in profileOwner.friends.all():
            context['can_show'] = False

        
        

        return context
    

