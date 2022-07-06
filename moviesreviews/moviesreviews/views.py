from email.headerregistry import Group
from django.forms import CharField, ChoiceField, ImageField, Textarea
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.files import File
from django.contrib.auth.models import Group

from movies.models import Movie
from users.models import UserProfile

def suggested_movies(user):
    users = UserProfile.objects.all()
    most_similars = sorted(users, key = (lambda u : u.similarity(user)))

    suggested_movies = set()

    for other_user in most_similars:
        watched_movies = Movie.objects.filter(reviews__in = other_user.reviews.all())
        for m in watched_movies:
            suggested_movies.add(m)
        if len(suggested_movies) >= 4:
            break

    
    return sorted(suggested_movies, key=(lambda m : len(m.stars())), reverse=True)[:4]

# Create your views here.
def home(request):
    last_added_movies = Movie.objects.order_by('-added_date')[:4]
    trend_movies = Movie.objects.all()
    trend_movies = sorted(trend_movies, key=(lambda m  : m.count_recent_views()), reverse=True)
    ctx = {'last_added' : last_added_movies, 'trend_movies' : trend_movies[:4]}
    sm = 0
    if request.user.is_authenticated:
        sm = suggested_movies(request.user.profile)
    ctx["suggested_movies"] = sm
    return render(request, template_name='home.html', context=ctx)

class CreateProfileForm(UserCreationForm):
    profile_img = ImageField(required=False, label='Immagine profilo(Opzionale)')
    bio = CharField(label='Biografia(Opzionale)', widget=Textarea, required=False)
    public_or_private = ChoiceField(label="Tipo profilo", choices=(('public', 'Pubblico'), ('private','Privato')))

    def save(self, commit= True):
        user = super().save(commit)
        user.groups.add(Group.objects.get(name="BaseUser"))
        profile = UserProfile()
        profile.user = user
        profile.bio = self.cleaned_data['bio']

        tmp_img = self.cleaned_data["profile_img"]
        if tmp_img == None:
            profile.profile_img.save("default.jpg", File(open("media/imgs/profileImgs/default.jpg", "rb")))
        else:
            profile.profile_img = tmp_img
            
        if self.cleaned_data['public_or_private'] == 'public':
            profile.is_user_page_public = True
        else:
            profile.is_user_page_public = False
        profile.save()
        return user

class UserCreateView(CreateView):
    form_class = CreateProfileForm
    template_name = 'user_create.html'
    success_url = reverse_lazy("login")

    
    

