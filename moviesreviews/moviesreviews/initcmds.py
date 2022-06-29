from movies.models import Genre, Movie, Person
from users.models import Review, UserProfile, Watch, Comment
from django.contrib.auth.models import User, Permission
from django.core.files import File
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

genres = ['giallo', 'horror', 'fantasy', 'animazione']
directors = [('1973-12-17','Rian Johnson'),
            ('1948-01-16','John Carpenter'),
            ('1961-10-31','Peter Jackson'),
            ('1962-12-23','Peter Ramsey')]
actors = [('1988-04-30','Ana de Armas'), 
            ('1958-11-22','Jamie Lee Curtis'), 
            ('1981-01-28','Elijah Wood'),
            ('1968-10-12','Hugh Jackman')]


def erase_db():
    print("Erase the DB")
    Movie.objects.all().delete()
    Person.objects.all().delete()
    Genre.objects.all().delete()
    User.objects.all().delete()


def create_dummies_movies(N):
    for n in range(N):
        create_movie('2019-05-10', 2015 + (n % 3), 'movie' + str(n), 90, 
        'Plot', 
        'default.jpg',
        genres[n % len(genres)],
        directors[n % len(directors)],
        actors[n % len(actors)])

def create_movie(added_date, release_year, title, duration, plot, cover, genre, director, cast):
    movie1 = Movie()
    movie1.added_date = added_date
    movie1.release_year = release_year
    movie1.title = title
    movie1.duration = duration
    movie1.plot = plot
    movie1.cover.save(cover, File(open("static/imgs/movies_covers/"+cover, "rb")))
    movie1.save()
    movie1.genre.set([Genre.objects.filter(name=genre).first()])
    movie1.directors.set([Person.objects.filter(name_surname=director).first()])
    movie1.cast.set([Person.objects.filter(name_surname=cast).first()])
    movie1.save()

def init_movies():
    if len(Movie.objects.all()) != 0 or len(Person.objects.all()) != 0 or len(Genre.objects.all()) != 0:
        return
    
    for g in genres:
        genre = Genre()
        genre.name = g
        genre.save()

    for d in directors:
        director = Person()
        director.birthday = d[0]
        director.name_surname = d[1]
        director.save()

    for a in actors:
        actor = Person()
        actor.birthday = a[0]
        actor.name_surname = a[1]
        actor.save()

    create_movie('2022-05-10', 2019, 'Cena con delitto', 130, 
    'Un investigatore e un soldato si recano in una lussureggiante tenuta per interrogare gli eccentrici parenti di un patriarca morto durante le celebrazioni del suo ottantacinquesimo compleanno.', 
    '0.jpg',
    'giallo',
    'Rian Johnson',
    'Ana de Armas')

    create_movie('2022-05-09', 1979, 'Halloween', 91, 
    "Un criminale già condannato per l'omicidio della sorella scappa di prigione e torna nella città natale in cerca della prossima vittima durante la notte di Halloween del 1978.", 
    '1.jpg',
    'horror',
    'John Carpenter',
    'Jamie Lee Curtis')

    create_movie('2022-05-08', 2019, "Il signore degli anelli: La compagnia dell'anello", 178, 
    "Un giovane hobbit e un variegato gruppo, composto da umani, un nano, un elfo e altri hobbit, partono per un delicata missione, guidati dal potente mago Gandalf. Devono distruggere un anello magico e sconfiggere il malvagio Sauron.", 
    '2.jpg',
    'fantasy',
    'Peter Jackson',
    'Jamie Lee Curtis')

    create_movie('2022-05-07', 2012, "Le 5 leggende", 97, 
    "La storia di un gruppo di eroi ben noti ai bambini, tra i quali Babbo Natale, il Coniglio Pasquale e la Fatina dei Denti, ognuno dotato di poteri straordinari, che devono unire le loro forze per proteggere le speranze dei bambini di tutto il mondo.", 
    '4.jpg',
    'animazione',
    'Peter Ramsey',
    'Hugh Jackman')

    create_dummies_movies(50)


users = [("Polylemma", "Polylemma"), ("Cheesecake", "Cheesecake"), ("SunnyPanda", "SunnyPanda")]
profiles = [('I am Polylemma', ["Cheesecake"], ["Cena con delitto", "Le 5 leggende"], False),
           ('I am Cheesecake', ["Polylemma", "SunnyPanda"], ["Halloween"], False),
           ('I am SunnyPanda', [], [], True) ]

watch_list = [('2022-05-14', 'Polylemma', 'Halloween'), 
        ('2022-05-12', 'Polylemma', 'Le 5 leggende'), 
        ('2022-05-14', 'Cheesecake', 'Halloween'),
        ('2021-05-14', 'Cheesecake', 'Halloween'),  
        ('2022-05-10', 'SunnyPanda', 'Halloween'), ]

review_list = [('2022-05-14', 'Polylemma', "Halloween", 'Film bello ma neanche troppo', 3),
                ('2022-05-12', 'Polylemma', "Le 5 leggende", 'Film fantastico', 5),
                ('2022-05-14', 'Cheesecake', "Halloween", 'Bello', 4),
                ('2022-05-10', 'SunnyPanda', "Halloween", 'Ok', 3),]

def init_users():
    admin = User.objects.filter(username = "admin").first()
    if admin is None:
        admin = User.objects.create_superuser("admin", "admin@admin.it", "admin")
        admin.save()
    if admin != None and not hasattr(admin, 'profile'):
        profile = UserProfile()
        profile.user = admin
        profile.bio = ""
        profile.profile_img.save('default.jpg', File(open("static/imgs/profiles_imgs/default.jpg", "rb")))
        watchlist = []
        profile.watch_list.set(watchlist)
        profile.is_user_page_public = p[3]
        profile.save()

    if len(User.objects.all()) != 0:
        return


    for u in users:
        user = User()
        user.username = u[0]
        user.password = u[0]
        user.save()
    
    for i in range(len(profiles)):
        p = profiles[i]
        profile = UserProfile()
        profile.user = User.objects.filter(username=users[i][0]).first()
        profile.save()
        profile.bio = p[0]
        profile.profile_img.save('default.jpg', File(open("static/imgs/profiles_imgs/default.jpg", "rb")))
        watchlist = []
        for s in p[2]:
            watchlist.append(Movie.objects.filter(title=s).first())
        profile.watch_list.set(watchlist)
        profile.is_user_page_public = p[3]
        profile.save()

    for i in range(len(profiles)):
        p = profiles[i]
        profile = User.objects.filter(username=users[i][0]).first().profile
        friends = []
        for s in p[1]:
            friends.append(User.objects.filter(username=s).first().profile)
        profile.friends.set(friends)

    for w in watch_list:
        watch = Watch()
        watch.date = w[0]
        watch.user = User.objects.filter(username=w[1]).first().profile
        watch.movie = Movie.objects.filter(title=w[2]).first()
        watch.save()

    for r in review_list:
        review = Review()
        review.date = r[0]
        review.owner = User.objects.filter(username=r[1]).first().profile
        review.movie = Movie.objects.filter(title=r[2]).first()
        review.body = r[3]
        review.rating = r[4]
        review.save()
    
    user = User.objects.filter(username='Cheesecake').first().profile
    review = Review.objects.filter(owner=user).first()
    comment = Comment()
    comment.date = '2022-05-14'
    comment.owner = User.objects.filter(username='Polylemma').first().profile
    comment.review = review
    comment.body = 'Non è vero'
    comment.save()

    comment = Comment()
    comment.date = '2022-05-14'
    comment.owner = User.objects.filter(username='SunnyPanda').first().profile
    comment.review = review
    comment.body = 'Concordo'
    comment.save()

    review.likes.set([User.objects.filter(username='SunnyPanda').first().profile])

        

def init_db():
    print("Init the DB")
    init_movies()
    init_users()

def init_groups():
    editors, created = Group.objects.get_or_create(name='Editor')
    base_users, created = Group.objects.get_or_create(name='BaseUser')
    content_type = ContentType.objects.get_for_model(Movie)
    post_permission = Permission.objects.filter(content_type=content_type)
    for perm in post_permission:
        if perm.codename == 'delete_movie':
            editors.permissions.add(perm)
        elif perm.codename == 'change_movie':
            editors.permissions.add(perm)
        elif perm.codename == 'add_movie':
            editors.permissions.add(perm)
        elif perm.codename == 'view_movie':
            editors.permissions.add(perm)
            base_users.permissions.add(perm)

    