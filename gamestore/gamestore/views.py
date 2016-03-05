from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from gamestore.models import *
from django.contrib.auth.models import User
from gamestore.forms import *

def index(request):
	games = Game.objects.filter(isPublic=True)
	if len(games) is 0:
		return render(request, 'front_page.html', {'games': []})
	else:
		games = sorted(games, key=lambda x: x.createDate, reverse=True)
		return render(request, 'front_page.html', {'games': games[:4]})

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
			user.userextension.save()
			return render(request, 'developerinfo.html', {})
		else:
			return render(request, 'auth_required.html', {'last_page': 'developerinfo'})
	else:
		return render(request, 'developerinfo.html', {})


def developerPage(request, user_name):

	if request.user.is_authenticated():
		if request.user.username == user_name:
			if request.user.userextension.isDeveloper == True:
				if request.method == 'POST':
					new_game_form = GameSubmissionForm(data=request.POST)
					if new_game_form.is_valid():
						newgame = new_game_form.save()
						newgame.developer = request.user
						newgame.save()
						ownedgame = GamesOwned(paymentState=PAYMENT_DEV, game=newgame)
						ownedgame.save()
						request.user.userextension.ownedGames.add(ownedgame)
						ownedgame.save()
						request.user.save()
						request.user.userextension.save()

						return redirect('/developer/' + request.user.username)
					else:
						return HttpResponse(new_game_form.errors)
					#	return redirect('/developerinfo') # TODO: Add some meaningful message to user.
				else:					
					developer = get_object_or_404(User, pk=request.user.id)
					games = Game.objects.filter(developer=developer)  
					new_game_form = GameSubmissionForm()
					context = {'user': developer, 'games': games, 'form': new_game_form}
					return render(request, 'developer_page.html', context)
			else:
				return redirect('/developerinfo')
				#return redirect('/user/' + request.user.username)
		else:
			raise PermissionDenied
	else:
		return render(request, 'auth_required.html', {'last_page': 'user'}) # TODO: change the context and html file name

def gameDeleteView(request, viewURL):
	if request.method == 'POST':
		game = get_object_or_404(Game, URL=view_URL)
		if game.developer == request.user:
			game.delete()
			return redirect('/developer/' + request.user.username)
		else:
			raise PermissionDenied
	else:
		raise PermissionDenied

def gameEditView(request, viewURL):
	if request.method == 'POST':
		game = get_object_or_404(Game, URL=view_URL)
		if game.developer == request.user:
			form = GameSubmissionForm(data=request.POST, instance=game)
			if form.is_valid():
				form.save()
				return redirect('/developer/' + request.user.username)
			else:
				return HttpResponse(form.errors)
		else:
			raise PermissionDenied
	else:
		raise PermissionDenied

def gameView(request, view_URL):
	user = request.user
	game = get_object_or_404(Game, URL=view_URL)
	owned = False
	if user.is_authenticated:
		userext = get_object_or_404(UserExtension, user=user)
		if len(GamesOwned.objects.filter(game=game, userextension=userext)) >= 1: # TODO: Check if this works
			owned = True
	context = {'user': user, 'game': game, 'owned': owned}
	return render(request, 'game.html', context)

def gamePlayView(request, view_URL):
	if request.user.is_authenticated():
		game = get_object_or_404(Game, URL=view_URL)
		context = {'game': game}
		return render(request, 'game_play.html', context)
	else:
		return render(request, 'auth_required.html', {'last_page': 'game', 'game': game})

def gameList(request):
	user = request.user
	games = Game.objects.filter(isPublic=True)
	genres = []
	for game in games:
		if game.genre not in genres:
			genres.append(game.genre)
	if len(genres) is 0:
		context = {'user': user, 'games': games, 'genres': genres}
	else:
		context = {'user': user, 'games': sorted(games, key=lambda x: x.name), 'genres': sorted(genres)}
	return render(request, 'game_list.html', context)

def test(request):
	users = User.objects.all()
	games = Game.objects.all()
	return render(request, 'test.html', {'users': users, 'games': games})
