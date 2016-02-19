from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)
    URL = models.URLfield(max_length=100)
    description = models.TextField() # TODO: Think about how to implement line feeds.
    # TODO: Other fields, e.g. link to dev, fk to dev, price, etc.
    
class GameSave(models.Model):
    data = models.TextField() # JSON data about the saved game.
    # TODO: Other fields, e.g. fk to game and user.
    
class Highscore(models.Model):
    data = models.TextField() # Score in JSON format.
    # TODO: Other fields, e.g. fk to game and user.
    
class GamesOwned(models.Model):
    paymentState = models.TextField() # Payment state in JSON???
    # TODO: Other fields, e.g. fk to game, user