from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# The class that is used to extend Django's User model. 
class UserExtension(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        parent_link=False)
    isDeveloper = models.BooleanField(default=False, editable=False)
    isValidated = models.BooleanField(default=False, editable=False) # Does not actually affect anything, but nice to have...
    ownedGames = models.ManyToManyField('GamesOwned')


# A list of game genres, to be used below.
GENRE_ACTION = 'Action'
GENRE_ADVENTURE = 'Adventure'
GENRE_FIGHTING = 'Fighting'
GENRE_MULTIPLAYER = 'Multiplayer'
GENRE_PLATFORM = 'Platform'
GENRE_PUZZLE = 'Puzzle'
GENRE_RACING = 'Racing'
GENRE_RPG = 'RPG'
GENRE_SHOOTER = 'Shooter'
GENRE_SIMULATION = 'Simulation'
GENRE_SPORTS = 'Sports'
GENRE_STRATEGY = 'Strategy'
GENRE_UNSPECIFIED = 'Other'

GAME_GENRES = (
    (GENRE_ACTION, 'Action'),
    (GENRE_ADVENTURE, 'Adventure'),
    (GENRE_FIGHTING, 'Fighting'),
    (GENRE_MULTIPLAYER, 'Multiplayer'),
    (GENRE_PLATFORM, 'Platform'),
    (GENRE_PUZZLE, 'Puzzle'),
    (GENRE_RACING, 'Racing'),
    (GENRE_RPG, 'RPG'),
    (GENRE_SHOOTER, 'Shooter'),
    (GENRE_SIMULATION, 'Simulation'),
    (GENRE_SPORTS, 'Sports'),
    (GENRE_STRATEGY, 'Strategy'),
    (GENRE_UNSPECIFIED, 'Other'),
)


URLAllowedChars = RegexValidator(r'^[0-9a-zA-Z~\.\-_]+$', 'Only alphanumeric characters and ~/./-/_ are allowed.')

# An instance of the Game model holds information about a single game on our service.
class Game(models.Model):
    name = models.CharField(max_length=80, verbose_name='game name')
    URL = models.CharField(max_length=150, unique=True, validators=[URLAllowedChars], verbose_name='game path (on our site)')
    gameSource = models.URLField(max_length=300, unique=True, verbose_name='game source URL')
    isPublic = models.BooleanField(default=False, verbose_name='is the game public? (You can always change this later)')
    genre = models.CharField(max_length=30, default=GENRE_UNSPECIFIED, choices=GAME_GENRES)
    description = models.TextField(blank=True) # TODO: Think about how to implement line feeds.
    image = models.URLField(blank=True, verbose_name='URL to image of game')
    image2 = models.URLField(blank=True, verbose_name='secondary image URL')
    developer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='price (€)')
    createDate = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updateDate = models.DateTimeField(auto_now=True, null=True, editable=False) # TODO: Not sure if works.
    

# The GameSave and Highscore models represent entries with data related to playing the game.  
class GameSave(models.Model):
    data = models.TextField(blank=True) # JSON data about the saved game.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    
class Highscore(models.Model):
    data = models.IntegerField(blank=False, null=False) # Score in JSON format.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    
# A list of payment states.
PAYMENT_SUCCESS = 'success'
PAYMENT_ERROR = 'error'
PAYMENT_CANCEL = 'cancel'
PAYMENT_DEV = 'dev'
PAYMENT_INPROGRESS = 'in_progress'
PAYMENT_NOT_STARTED = 'not_started'

PAYMENT_STATES = (
    (PAYMENT_SUCCESS, 'Success'),
    (PAYMENT_ERROR, 'Error'),
    (PAYMENT_CANCEL, 'Canceled'),
    (PAYMENT_DEV, 'Developer'),
    (PAYMENT_INPROGRESS, 'In Progress'),
    (PAYMENT_NOT_STARTED, 'Not started'),
)

# A GamesOwned instance represents a single purchase by a single user.
# It is only used for successfully purchased or submitted games.
class GamesOwned(models.Model):
    paymentState = models.TextField(default=PAYMENT_NOT_STARTED, choices=PAYMENT_STATES) # Payment state; success, error, cancel, developer, etc
    createDate = models.DateTimeField(auto_now_add=True, null=True)
    updateDate = models.DateTimeField(auto_now=True, null=True) # TODO: Not sure if works.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE) 
    # Should users know about owned games which have been deleted?
    # If so, the on_delete value for the fk should be models.SET_NULL
    


