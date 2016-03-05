from django import forms
from django.forms import ModelForm, TextInput, URLInput, Textarea
from django.contrib.auth.models import User
from gamestore.models import Game

class UserForm(ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class UserEditForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class GameSubmissionForm(ModelForm):
    
    class Meta:
        model = Game
        
        fields = ['name', 'URL', 'gameSource', 'genre', 'description', 'price', 'image', 'image2', 'isPublic']
        widgets = {
            'name': TextInput(attrs={'size': 40}),
            'URL': TextInput(attrs={'size': 28}),
            'gameSource': URLInput(attrs={'size': 34}),
            'description': Textarea(attrs={'rows': 10}),
            'image': URLInput(attrs={'size': 40}),
            'image2': URLInput(attrs={'size': 40}),
        }

class GameEditingForm(ModelForm):
    
    class Meta:
        model = Game
        
        fields = ['name', 'gameSource', 'genre', 'description', 'price', 'image', 'image2', 'isPublic']
        # Label does not work; field name different; cols can't be adjusted dynamically based on page width.
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20, 'label': 'Awesome description!'}),
        }


