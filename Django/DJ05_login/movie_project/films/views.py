from django.shortcuts import render, redirect
from .models import Movie
from .forms import CustomUserCreationForm, MovieForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    return render(request, 'films/home.html')  # Страница-приветствие для незалогиненных

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'films/add_movie.html', {'form': form})

@login_required
def movie_list(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, 'films/movie_list.html', {'movies': movies})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})