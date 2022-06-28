from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, Select
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from movies.models import Genre, Movie
from django.db.models import Count, Sum
from datetime import datetime
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
def new_review(request):
    user = get_object_or_404(User, username=request.user)
    form = ReviewForm(request.POST)
    update = False
    if (form.is_valid()):
        movie_pk = request.POST.get("movie-pk")
        movie = get_object_or_404(Movie, pk = movie_pk)
        reviews = Review.objects.filter(owner = user.profile, movie = movie)
        if len(reviews) > 0:
            r = reviews.first()
            r.date = timezone.now()
            r.body = form.cleaned_data['body']
            r.rating = int(form.cleaned_data['rating'])
            r.save()
            update = True
        else:
            review = Review()
            review.owner = user.profile
            review.movie = movie
            review.rating = int(form.cleaned_data['rating'])
            review.date = timezone.now()
            review.body = form.cleaned_data['body']
            review.save()
    response = redirect(reverse('movies:moviedetails', args=[movie_pk]))
    if update:
        response["Location"] += "?reviewUpdated=true"
    else:
        response["Location"] += "?reviewAdded=true"
    return response

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

@login_required
def new_comment(request):
    user = get_object_or_404(User, username=request.user)
    review = get_object_or_404(Review, pk = request.POST["review-pk"])
    movie_pk = request.POST["movie-pk"]
    form = CommentForm(request.POST)
    if (form.is_valid()):
        comment = Comment()
        comment.owner = user.profile
        comment.review = review
        comment.body = form.cleaned_data["body"]
        comment.date = timezone.now()
        comment.save()
    response = redirect(reverse('movies:moviedetails', args=[movie_pk]))
    response["Location"] += "?commentAdded=true"
    return response

@login_required
def delete_comment(request):
    user = get_object_or_404(User, username=request.user)
    comment = get_object_or_404(Comment, pk = request.POST["comment-pk"])
    movie_pk = request.POST["movie-pk"]
    if (user.profile == comment.owner):
        comment.delete()
    response = redirect(reverse('movies:moviedetails', args=[movie_pk]))
    response["Location"] += "?commentDeleted=true"
    return response

@login_required
def add_to_watchlist(request):
    user = get_object_or_404(User, username=request.user)
    movie_pk = request.GET.get("movie-pk")
    movie = get_object_or_404(Movie, pk = movie_pk)
    r_text = "added"
    if movie in user.profile.watch_list.all():
        user.profile.watch_list.remove(movie)
        r_text = "removed"
    else:
        user.profile.watch_list.add(movie)

    return HttpResponse(r_text)

@login_required
def delete_review(request):
    user = get_object_or_404(User, username=request.user)
    movie_pk = request.POST.get("movie-pk")
    movie = get_object_or_404(Movie, pk = movie_pk)
    review = get_object_or_404(Review, owner = user.profile, movie = movie)
    review.delete()
    response = redirect(reverse('movies:moviedetails', args=[movie_pk]))
    response["Location"] += "?reviewDeleted=true"
    return response

@login_required
def remove_from_watchlist(request):
    user = get_object_or_404(User, username=request.user)
    movie_pk = request.POST.get("movie-pk")
    movie = get_object_or_404(Movie, pk = movie_pk)
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
def add_remove_friend(request):
    my_user = get_object_or_404(User, pk = request.user.pk)
    my_profile = get_object_or_404(UserProfile, user = my_user)

    other_profile = get_object_or_404(UserProfile, pk = request.POST.get('profile-pk', None))

    if my_profile == other_profile:
        return redirect(reverse('users:profile_details', args=[other_profile.pk]))

    action = "added"
    if other_profile in my_profile.friends.all():
        my_profile.friends.remove(other_profile)
        action = "removed"
    else:
        my_profile.friends.add(other_profile)

    if (request.POST.get('to-friends', None) != None):
        return redirect(reverse('users:friends', args=[my_profile.pk]))
    response = redirect(reverse('users:profile_details', args=[other_profile.pk]))
    response["Location"] += '?action=' + action
    return response


class ProfileDetails(LoginRequiredMixin,DetailView):
    model = UserProfile
    template_name = 'users/profileDetails.html'

    def formatWatchtime(watchtime):
        if watchtime == None:
            return "0 m"
        if watchtime < 60:
            return str(watchtime) + " m"
        h = watchtime // 60
        m = watchtime % 60
        return str(h) + " h " + str(m) + " m"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_owner = context["object"]
        context['can_show'] = True
        context['favourite_movie'] = None
        context['favourite_genre'] = None
        context['watchtime'] = None

        # Favourite movie
        watches = Watch.objects.filter(user=profile_owner).values("movie").annotate(mcount = Count("movie")).order_by("-mcount")
        if len(watches.all()) > 0:
            w = watches.all().first()
            context['favourite_movie'] = get_object_or_404(Movie, pk = w["movie"])

        # Favourite genre
        watches = Watch.objects.filter(user=profile_owner).values("movie")
        movies = Movie.objects.filter(pk__in = watches).values("genre").annotate(gcount = Count("genre")).order_by("-gcount")
        if len(movies.all()) > 0:
            m = movies.all().first()
            context['favourite_genre'] = get_object_or_404(Genre, pk = m["genre"])
        
        
        # Watch time
        watches = Watch.objects.filter(user=profile_owner).filter(date__gt = (timezone.now() - datetime.timedelta(days=30))).values("movie")
        movies = Movie.objects.filter(pk__in = watches).aggregate(Sum('duration'))
        if len(movies) > 0:
            context['watchtime'] = ProfileDetails.formatWatchtime(movies["duration__sum"])
        

        if profile_owner.is_user_page_public:
            return context

        user = get_object_or_404(User, pk = self.request.user.pk)
        profile = get_object_or_404(UserProfile, user = user)

        if profile != profile_owner and profile not in profile_owner.friends.all():
            context['can_show'] = False

        return context



@login_required    
def add_watch(request):
    movie_pk = request.POST.get('movie-pk', None)
    if movie_pk == "":
        movie_pk = None
    movie = get_object_or_404(Movie, pk = movie_pk)
    profile = request.user.profile
    date_s = request.POST.get('watchdate', None)
    status = 'failed'
    if date_s != None:
        watch = Watch()
        watch.user = profile
        watch.movie = movie
        watch.date = date_s
        watch.save()
        status = 'ok'

    response = redirect(reverse('movies:moviedetails', args=[movie_pk]))
    response['Location'] += '?addwatch=' + status
    return response

class FriendsPage(LoginRequiredMixin,DetailView):
    model = UserProfile
    template_name = 'users/friendsPage.html'

    def get(self, request, *args, **kwargs):
        response = super(FriendsPage, self).get(request, *args, **kwargs)
        obj = self.object
        user = get_object_or_404(User, pk = self.request.user.pk)
        profile = get_object_or_404(UserProfile, user = user) 
        if obj != profile and not obj.is_user_page_public and profile not in obj.friends.all():
            return redirect(reverse("users:profile_details", args=[obj.pk]))

        return response
    


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['profile_img', 'bio', 'is_user_page_public']
    template_name = 'users/updateUser.html'

    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse('users:profile_details', args=[self.object.pk]) + "?updated=true"

class SearchProfile(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'users/search.html'

    def get_queryset(self):
        username = self.request.GET.get('username', None)
        if username == None:
            return UserProfile.objects.all()
        users = User.objects.filter(username__icontains = username).all()
        return UserProfile.objects.filter(user__in = users)

@login_required        
def upgrade_or_downgrade(request):
    if not request.user.is_superuser:
        return redirect(reverse("home"))
    
    user_pk = request.POST.get("user-pk", None)
    user = get_object_or_404(User, pk = user_pk)

    editor_group = Group.objects.filter(name = "Editor").first()

    if editor_group in user.groups.all():
        user.groups.remove(editor_group)
    else:
        user.groups.add(editor_group)
    
    return redirect(reverse("users:profile_details", args=[user.profile.pk]))