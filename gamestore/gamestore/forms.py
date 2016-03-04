from django import forms
from django.contrib.auth.models import User, Game

class UserForm(forms.ModelForm):
	
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User

		fields = ['username', 'email', 'password']


class GameSubmitForm(forms.ModelForm):
	
	class Meta:
		model = Game

		fields = ['name', 'URL', 'password']

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
