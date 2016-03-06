from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from gamestore.models import *
from django.contrib.auth.models import User
from gamestore.forms import *
from hashlib import md5
import json
PAYMENT_SECRET_KEY = 'ed1c50ac3b75bd1aa70835c8c84007ed'


def index(request):
    games = Game.objects.filter(isPublic=True)
    if request.user.is_authenticated(): # Retroactively create userextensions to external login users.
        if not UserExtension.objects.filter(user=request.user):
            userext = UserExtension(user=request.user, isDeveloper=False, isValidated=True)
            userext.save()
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
#            if user.email: # Email disabled because we don't have an SMTP backend.
#                send_mail(
#                    # Subject
#                    'Validate your Quagmire Zone Underground account',
#                    # Message
#                    'Hi, and thank you for joining Quagmire Zone Underground.\n\nPlease use the following URL to validate your account.\n\nhttp://localhost:8000/user/' + user.username + '/validate?key=' + md5(str(user.id).encode('ascii')).hexdigest() + '\n\nThis message is safe to ignore if you received by error. Please do not share the link with anyone.\n\nBest Regards,\nQuagmire Zone Underground',
#                    # Sender
#                    'no-reply@quagmire.com',
#                    # Recipients
#                    [user.email],
#                    # Fail silently?
#                    fail_silently=False)
            return redirect(index)
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'form': user_form})


def userValidation(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if (request.GET.get('key', 'false') == md5(str(user.id).encode('ascii')).hexdigest()):
        user.userextension.isValidated = True # Does not actually affect anything...
        user.save()
        user.userextension.save()
        return redirect('/user/' + user_name) 
    else:
        return HttpResponseBadRequest("It seems like your validation URL is not correct.")


def userPage(request, user_name):
    if request.user.is_authenticated():
        if request.user.username == user_name:
            errors = {}
            if request.method == 'POST':
                user_form = UserEditForm(data=request.POST, instance=request.user)
                if user_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    return redirect('/user/' + request.user.username)
                else:
                    errors.update(user_form.errors)
            user = get_object_or_404(User, pk=request.user.id)
            userext = get_object_or_404(UserExtension, user=user)
            gamesOwned = GamesOwned.objects.filter(userextension=userext)
            games = [elem.game for elem in gamesOwned]
            user_form = UserEditForm(instance=request.user)
            context = {'user': user, 'games': sorted(games, key=lambda x: x.name), 'form': user_form, 'errors': errors}
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
                added_now = False
                errors = {}
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
                        added_now = True
                    else:
                        errors.update(new_game_form.errors)
                developer = get_object_or_404(User, pk=request.user.id)
                games = Game.objects.filter(developer=developer)
                gamesBought = GamesOwned.objects.filter(paymentState=PAYMENT_SUCCESS)
                boughtGames = []
                for boughtGame in sorted(gamesBought, key=lambda x: (x.game.name, x.createDate)):
                    if boughtGame.game in games:
                        boughtGames.append(boughtGame)
                add_game_form = GameSubmissionForm()
                game_editing_forms = []
                for x in games:
                    editing_form = GameSubmissionForm(instance=x)
                    editing_form.fields['URL'].widget.attrs['readonly'] = True
                    game_editing_forms.append(editing_form)
                gameforms = zip(games, game_editing_forms)
                context = {'user': developer, 'form': add_game_form, 'gameforms': gameforms, 'boughtgames': boughtGames, 'added_now': added_now, 'errors': errors}
                return render(request, 'developer_page.html', context)
            else:
                return redirect('/developerinfo')
        else:
            raise PermissionDenied
    else:
        return render(request, 'auth_required.html', {'last_page': 'user'}) # TODO: change the context


def gameView(request, view_URL):
	user = request.user
	game = get_object_or_404(Game, URL=view_URL)
	purchased_now = False
	owned = False
	highscores = Highscore.objects.filter(game=game)
	players = User.objects.all()
	playerscores = []
	for player in players:
		personalscores = sorted(highscores.filter(user=player), key=lambda x: x.data)
		if len(personalscores) >= 1:
			playerscores.append(personalscores[0])

	pid = md5(('user: ' + str(user.id) + ', game: ' + str(game.id)).encode('ascii')).hexdigest()
	
	# If game was just purchased...
	if request.GET.get('pid', '') and request.GET.get('ref', '') and request.GET.get('result', '') and request.GET.get('checksum', ''):
		if request.GET.get('result', '') == 'success':
			if md5("pid={}&ref={}&result={}&token={}".format(pid, request.GET.get('ref', ''), 'success', PAYMENT_SECRET_KEY).encode('ascii')).hexdigest() == request.GET.get('checksum', 'a'): # TODO: Raise PermissionDenied if hashes do not match
				purchasedgame = GamesOwned(paymentState=PAYMENT_SUCCESS, game=game)
				purchasedgame.save()
				request.user.userextension.ownedGames.add(purchasedgame)
				request.user.save()
				request.user.userextension.save()
				purchased_now = True
	
	# The page itself
	p_info = {}
	if user.is_authenticated():
		userext = get_object_or_404(UserExtension, user=user)
		gameOwned = GamesOwned.objects.filter(game=game, userextension=userext)
		if gameOwned: # TODO: Does not respect payment status (!!!)
			owned = True
		else:
			p_info.update({
				'payment_id': pid,
				'seller_id': 'quagmire',
				'success_url': 'http://localhost:8000/game/' + game.URL, # TODO: Change to Heroku URL
				'cancel_url': 'http://localhost:8000/game/' + game.URL,
				'error_url': 'http://localhost:8000/game/' + game.URL,
				'checksum': md5("pid={}&sid={}&amount={}&token={}".format(pid, 'quagmire', game.price, PAYMENT_SECRET_KEY).encode('ascii')).hexdigest(), # TODO: TEST WITH FAILED PAYMENT BY SETTING 'dev' TO TRUE
				'amount': game.price,
			})
	if game.isPublic or owned:
		context = {'user': user, 'game': game, 'purchased_now': purchased_now, 'owned': owned, 'highscores': sorted(playerscores, key=lambda y: -y.data), 'purchase_info': p_info}
		return render(request, 'game.html', context)
	else:
		raise PermissionDenied


def gamePlayView(request, view_URL):
	if request.user.is_authenticated():
		game = get_object_or_404(Game, URL=view_URL)
		userext = get_object_or_404(UserExtension, user=request.user)
		gameOwned = GamesOwned.objects.filter(game=game, userextension=userext)
		if gameOwned:
			context = {'game': game}
			return render(request, 'game_play.html', context)
		else:
			raise PermissionDenied
	else:
		return render(request, 'auth_required.html', {}) # TODO: 'last_page': 'game', 'game': game


# Unused view for deleting games.
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


def gameEditView(request, view_URL):
    if request.method == 'POST':
        game = get_object_or_404(Game, URL=view_URL)
        if game.developer == request.user:
            form = GameEditingForm(data=request.POST, instance=game)
            if form.is_valid():
                form.save()
                return redirect('/developer/' + request.user.username)
            else:
                return render(request, 'error.html', {})
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def gameStatsAPIhandling(request, view_URL):
    if request.GET.get('format', '').lower() == 'json' and request.GET.get('action', '').lower() == 'highscores':
        amount = int(request.GET.get('amount', '10'))
        context = {'action': 'highscores', 'format': 'JSON', 'amount': amount}
        scores = []
        game = get_object_or_404(Game, URL=view_URL)
        highscores = Highscore.objects.filter(game=game)
        players = User.objects.all()
        playerscores = []
        for player in players:
            personalscores = sorted(highscores.filter(user=player), key=lambda x: x.data)
            if len(personalscores) >= 1:
                playerscores.append(personalscores[0])
        playerscores = sorted(playerscores, key=lambda x: -x.data) # TODO: Might break on highscores
        playerscores = playerscores[:amount]
        playerscores[:] = map(lambda x: {'score': x.data, 'user': x.user.username, 'game': x.game.name}, playerscores)
        context.update({'scores': json.dumps(playerscores)})
        return render(request, 'restful_stats.html', context)
    else:
        return HttpResponseBadRequest("Bad request to the API.")


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
	highscores = Highscore.objects.all()
	gamesaves = GameSave.objects.all()
	return render(request, 'test.html', {'users': users, 'games': games, 'highscores': highscores, 'gamesaves': gamesaves})


def postScore(request):
	data = json.loads(request.body.decode('UTF-8'))
	game_id = data['game_id']
	score = int(data['score'])
	game = get_object_or_404(Game, URL=game_id)
	user = request.user

	highscore = Highscore.objects.filter(user=user, game=game)

	if len(highscore)>0:
		if highscore[0].data < score:
			highscore[0].data = score
			highscore[0].save()
	else:
		highscore = Highscore(game=game, user=user, data=score)
		highscore.save()
	context = {'message': 'Score saved succesfully!'}
	return JsonResponse(context)


def saveState(request):
    data = json.loads(request.body.decode('UTF-8'))
    game_id = data['game_id']
    state = data['gameState']
    game = get_object_or_404(Game, URL=game_id)
    user = request.user
    
    save = GameSave.objects.filter(user=user, game=game)
    
    if save:
        save[0].data = state
        save[0].save()
    else:
        save = GameSave(game=game, user=user, data=state)
        save.save()
    context = {'message': 'Game saved succesfully!'}
    return JsonResponse(context)


def loadRequest(request):
    data = json.loads(request.body.decode('UTF-8'))
    game_id = data['game_id']
    game = get_object_or_404(Game, URL=game_id)
    user = request.user
    
    save = GameSave.objects.filter(user=user, game=game)
    
    if save:
        response = {'messageType': 'LOAD', 'gameState': save[0].data}
        context = {'response': response}
        return JsonResponse(context)
    else:
        response = {'messageType': 'ERROR', 'info': 'Unable to load the game state.'}
        context = {'response': response}
        return JsonResponse(context)
        
    
def sameOrigin(request):
    return render(request, 'sameorigin.html', {})


