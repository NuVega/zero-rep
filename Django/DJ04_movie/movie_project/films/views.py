from django.shortcuts import render, redirect
from .models import Movie

def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        review = request.POST['review']
        Movie.objects.create(title=title, description=description, review=review)
        return redirect('movie_list')
    return render(request, 'films/add_movie.html')

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'films/movie_list.html', {'movies': movies})