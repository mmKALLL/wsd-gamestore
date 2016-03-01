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
from django.conf.urls import url
from django.contrib import admin
from gamestore import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^user/([0-9a-zA-Z]+)$', views.userPage),
    url(r'^developer/([0-9a-zA-Z]+)$', views.developerPage),
    url(r'^game/([0-9]+)$', views.gameView), # TODO: Change number to the name of the game
    url(r'^game/([0-9]+)/play$', views.gamePlayView),
    url(r'^gamelist$', views.gameList),
    url(r'^test$', views.test)
]
