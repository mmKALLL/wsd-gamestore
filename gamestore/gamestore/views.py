from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from gamestore.forms import UserForm
from django.contrib.auth.models import User  #TODO: Check if this includes UserExtension
from gamestore.models import *

def index(request):
	return render(request, 'front_page.html', {}) # TODO: Possibly change HTML name???

def register(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			userextension = UserExtension(user=user)
			userextension.save()
			return redirect(index)
	else:
		user_form = UserForm()
	return render(request, 'register.html', {'form': user_form})

def userPage(request, user_name):
	if request.user.is_authenticated():
		if request.user.username == user_name:
			user = get_object_or_404(User, pk=request.user.id)
			userext = get_object_or_404(UserExtension, user=user)
			gamesOwned = GamesOwned.objects.filter(userextension=userext)
			games = [elem.game for elem in gamesOwned]
			context = {'user': user, 'games': games}
			return render(request, 'user.html', context)
		else:
			raise PermissionDenied
	else:
		return render(request, 'auth_required.html', {'last_page': 'user'}) # TODO: change the context and html file name

def developerInfoPage(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			user = request.user
			user.userextension.isDeveloper = True
			user.save()
		else:
			return render(request, 'auth_required.html', {'last_page': 'developerinfo'})
	else:
		return render(request, 'developerinfo.html', {})


def developerPage(request, user_name):
	if request.user.is_authenticated():
		if request.user.username == user_name:
			if request.user.userextension.isDeveloper == True:
				developer = get_object_or_404(User, pk=request.user.id)
				games = get_list_or_404(Game, developer=developer)  
				context = {'user': developer, 'games': games}
				return render(request, 'developer_page.html', context)
			else:
				return redirect('/user/' + request.user.username)
		else:
			raise PermissionDenied
	else:
		return render(request, 'auth_required.html', {'last_page': 'user'}) # TODO: change the context and html file name

def gameView(request, game_id):
	user = request.user
	game = get_object_or_404(Game, pk=game_id)
	context = {'user': user, 'game': game}
	return render(request, 'game.html', context)

def gamePlayView(request, game_id):
	if request.user.is_authenticated():
		game = get_object_or_404(Game, pk=game_id)
		context = {'game': game}
		return render(request, 'game_play.html', context)
	else:
		return render(request, 'auth_required.html', {'last_page': 'game', 'game': game})

def gameList(request):
	user = request.user
	games = Game.objects.filter(isPublic=True)
	genres = ['Unspecified']
	for game in games:
		if game.genre not in genres:
			genres.append(game.genre)
	context = {'user': user, 'games': sorted(games), 'genres': sorted(genres)}
	return render(request, 'game_list.html', context)

def test(request):
	users = User.objects.all()
	games = Game.objects.all()
	return render(request, 'test.html', {'users': users, 'games': games})
