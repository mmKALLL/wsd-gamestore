from django.http import HttpResponse, Http404, Http403
from django.shortcuts import render

def index(request):
	return render(request, 'front_page.html', {}) # TODO: Possibly change HTML name???

def register(request):
	return render(request, 'register.html', {})

def userPage(request, user_id):
	if request.user.is_authenticated():
		if request.user.id is user_id:
			user = get_object_or_404(User, pk=user_id)
			games = get_list_or_404() # TODO: Get list of games for user
			context = {'user': user, 'games': games}
			return render(request, 'user.html', context)
		else:
			return Http403
	else:
		return render(request, 'auth_required.html', {'last_page': 'user'}) # TODO: change the context and html file name


def developerPage(request, user_id):
	if request.user.is_authenticated():
		if request.user.id is user_id:
			# TODO: Check if user is dev
			developer = get_object_or_404(User, pk=user_id)
			games = get_list_or_404()  # TODO: Get list of games that the developer has made   
			context = {'user': developer, 'games': games}
			return render(request, 'developer_page.html', context)
		else:
			return Http403
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
	games = Game.objects.all()
	context = {'user': user, 'games': games}
	return render(request, 'game_list.html', context)	