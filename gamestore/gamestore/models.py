from django.db import models

# TODO: Users should have a ManyToManyField with GamesOwned !!!

class Game(models.Model):
    name = models.CharField(max_length=50)
    URL = models.URLField(max_length=150)
    description = models.TextField(blank=True) # TODO: Think about how to implement line feeds.
    developer = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        null=True)
    price = models.DecimalField(max_digits=None, decimal_places=2)
    
class GameSave(models.Model):
    data = models.TextField(blank=True) # JSON data about the saved game.
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE)
    
class Highscore(models.Model):
    data = models.TextField() # Score in JSON format.
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE)
    
class GamesOwned(models.Model):
    paymentState = models.TextField() # Payment state in JSON???
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE) 
    # Should users know about owned games which have been deleted?
    # If so, the on_delete value for the fk should be models.SET_NULL
    



