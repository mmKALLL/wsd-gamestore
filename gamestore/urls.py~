"""gamestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from gamestore import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^user/([0-9a-zA-Z@\.+\-_]+)/validate$', views.userValidation),
    url(r'^user/([0-9a-zA-Z@\.+\-_]+)$', views.userPage),
    url(r'^developerinfo$', views.developerInfoPage),
    url(r'^developer/([0-9a-zA-Z@\.+\-_]+)$', views.developerPage),
    url(r'^game/([0-9a-zA-Z~\.\-_]+)/delete$', views.gameDeleteView),
    url(r'^game/([0-9a-zA-Z~\.\-_]+)/edit$', views.gameEditView),
    url(r'^game/([0-9a-zA-Z~\.\-_]+)/play$', views.gamePlayView),
    url(r'^game/([0-9a-zA-Z~\.\-_]+)/stats$', views.gameStatsAPIhandling),
    url(r'^game/([0-9a-zA-Z~\.\-_]+)$', views.gameView),
    url(r'^gamelist$', views.gameList),
    url(r'^post_score$', views.postScore, name='post_score'),
    url(r'^save_state$', views.saveState, name='save_state'),
    url(r'^load_request$', views.loadRequest, name='load_request'),
    url("^soc/", include("social.apps.django_app.urls", namespace="social")),
    url(r'^test$', views.test),
    url(r'^sameorigin$', views.sameOrigin)
]
