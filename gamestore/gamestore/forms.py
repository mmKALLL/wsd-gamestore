from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from gamestore.models import Game

class UserForm(ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    

class GameSubmissionForm(forms.ModelForm):
    
    class Meta:
        model = Game
        
        fields = ['name', 'URL', 'gameSource', 'genre', 'description', 'price', 'image', 'image2', 'isPublic']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20, 'label': 'Awesome description!'}),
        }


