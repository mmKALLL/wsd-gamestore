from django.db import models
from django.contrib.auth.models import User

class UserExtension(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        parent_link=False)
    isDeveloper = models.BooleanField(default=False)
    ownedGames = models.ManyToManyField('GamesOwned')
    

class Game(models.Model):
    name = models.CharField(max_length=80, default=id)
    URL = models.URLField(max_length=150, unique=True, default=id)
    gameSource = models.URLField(max_length=300, unique=True, blank=True)
    isPublic = models.BooleanField(default=False)
    genre = models.CharField(max_length=30, default='Unspecified')
    description = models.TextField(blank=True) # TODO: Think about how to implement line feeds.
    image = models.URLField(blank=True)
    image2 = models.URLField(blank=True)
    developer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    
class GameSave(models.Model):
    data = models.TextField(blank=True) # JSON data about the saved game.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    
class Highscore(models.Model):
    data = models.TextField() # Score in JSON format.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    
class GamesOwned(models.Model):
    paymentState = models.TextField() # Payment state in JSON???
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE) 
    # Should users know about owned games which have been deleted?
    # If so, the on_delete value for the fk should be models.SET_NULL
    



