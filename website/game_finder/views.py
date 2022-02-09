from django.shortcuts import render
from django.http import HttpResponse
from .models import Game
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    return render(request, 'game_finder/home.html')

def search(request):
    # if request.method == 'POST':
    #     searched = request.POST['searched']
    #     games = Game.objects.filter(name__contains=searched)
    #     p = Paginator(games, 5)
    #     page = request.GET.get('page')
    #     g_list = p.get_page(page)
    #     return render(request, 'game_finder/search.html', {'searched':searched, 'games':games, 'g_list':g_list})
    # else:
    #     return render(request, 'game_finder/search.html')
    if request.method =='GET':
        if request.GET.get('instock') == 'yes':
            game_search = request.GET.get('searched').upper()
            games = Game.objects.filter(name__contains=game_search, status=True).order_by('price', 'name', '-status')
            p = Paginator(games, 5)
            page = request.GET.get('page')
            g_list = p.get_page(page)
            return render(request, 'game_finder/search.html', {'game_search':game_search, 'games':games, 'g_list':g_list})
        game_search = request.GET.get('searched').upper()
        games = Game.objects.filter(name__contains=game_search).order_by('price', 'name', '-status')
        p = Paginator(games, 5)
        page = request.GET.get('page')
        g_list = p.get_page(page)
        return render(request, 'game_finder/search.html', {'game_search':game_search, 'games':games, 'g_list':g_list})
    else:
        return render(request, 'game_finder/search.html')

def whomade(request):
    return render(request, 'game_finder/whomade.html')

def about(request):
    return render(request, 'game_finder/about.html')