import json
from movies.models import Genre, Movie, Person
from .settings import BASE_DIR, STATIC_URL

genres = ['giallo', 'horror', 'fantasy']
directors = [('1973-12-17','Rian Johnson'),
            ('1948-01-16','John Carpenter'),
            ('1961-10-31','Peter Jackson')]
actors = [('1988-04-30','Ana de Armas'), 
            ('1958-11-22','Jamie Lee Curtis'), 
            ('1981-01-28','Elijah Wood')]


def erase_db():
    print("Erase the DB")
    Movie.objects.all().delete()
    Person.objects.all().delete()
    Genre.objects.all().delete()

def init_db():
    print("Init the DB")
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
        actor.birthday = d[0]
        actor.name_surname = d[1]
        actor.save()

    movie1 = Movie()
    movie1.added_date = '2022-05-10'
    movie1.release_year = 2019
    movie1.title = 'Cena con delitto'
    movie1.plot = 'Un investigatore e un soldato si recano in una lussureggiante tenuta per interrogare gli eccentrici parenti di un patriarca morto durante le celebrazioni del suo ottantacinquesimo compleanno.'
    movie1.cover_path = STATIC_URL + "imgs/movies_covers/0.jpg"
    movie1.save()
    movie1.genre.set([Genre.objects.filter(name='giallo').first()])
    movie1.directors.set([Person.objects.filter(name_surname='Rian Johnson').first()])
    movie1.cast.set([Person.objects.filter(name_surname='Ana de Armas').first()])

    movie1 = Movie()
    movie1.added_date = '2022-05-09'
    movie1.release_year = 1979
    movie1.title = 'Halloween'
    movie1.plot = "Un criminale già condannato per l'omicidio della sorella scappa di prigione e torna nella città natale in cerca della prossima vittima durante la notte di Halloween del 1978."
    movie1.cover_path = STATIC_URL + "imgs/movies_covers/1.jpg"
    movie1.save()
    movie1.genre.set([Genre.objects.filter(name='horror').first()])
    movie1.directors.set([Person.objects.filter(name_surname='John Carpenter').first()])
    movie1.cast.set([Person.objects.filter(name_surname='Ana de Armas').first()])
    
    movie1 = Movie()
    movie1.added_date = '2022-05-08'
    movie1.release_year = 2019
    movie1.title = "Il signore degli anelli: La compagnia dell'anello"
    movie1.plot = "Un giovane hobbit e un variegato gruppo, composto da umani, un nano, un elfo e altri hobbit, partono per un delicata missione, guidati dal potente mago Gandalf. Devono distruggere un anello magico e sconfiggere il malvagio Sauron."
    movie1.cover_path = STATIC_URL + "imgs/movies_covers/2.jpg"
    movie1.save()
    movie1.genre.set([Genre.objects.filter(name='giallo').first()])
    movie1.directors.set([Person.objects.filter(name_surname='Peter Jackson').first()])
    movie1.cast.set([Person.objects.filter(name_surname='Elijah Wood').first()])

    