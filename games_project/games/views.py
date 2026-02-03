from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Game

class GameListView(ListView):
    model = Game
    template_name = "games/list.html"
    context_object_name = "games"

class GameDetailsView(DetailView):
    model = Game
    template_name = "games/detail.html"
    context_object_name = "game" 

