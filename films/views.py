from django.views.generic import ListView, DetailView, View
from .models import Film, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .forms import UserForm
import random
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages


class IndexView(ListView):
    model = Film
    context_object_name = 'films_db'
    # print(Film.objects.all().order_by('-release_date')[:9])

    def get_queryset(self):
        return Film.objects.all().order_by('-release_date')[:9]

    template_name = 'films/index.html'


class Detail_view(DetailView):
    model = Film
    context_object_name = 'film'
    template_name = 'films/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail_view, self).get_context_data(**kwargs)
        hours = int(self.object.duration) // 60
        minutes = (int(self.object.duration) - hours * 60) % 60
        context['comments'] = context['film'].comment_set.all()
        context['actors_list'] = self.object.actors.split(", ")
        context['genre_list'] = self.object.genre.split(", ")
        context['duration'] = f'{hours} {"hours" if hours != 1 else "hour"} {minutes} {"minutes" if minutes != 1 else "minute"}'
        return context


class GenreListView(ListView):
    model = Film
    context_object_name = 'films_db'
    template_name = 'films/genres.html'

    def get_queryset(self):
        print(self.kwargs['genre'])
        return Film.objects.filter(genre__contains=self.kwargs['genre'].capitalize())

    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by')
        page = self.request.GET.get('page')
        direction = self.request.GET.get('direction')
        ordering = order_by
        if direction == 'desc':
            ordering = '-{}'.format(ordering)
        films = Film.objects.filter(genre__contains=self.kwargs['genre'].capitalize()).order_by(ordering)

        paginator = Paginator(films, 60)
        try:
            visible_films = paginator.page(page)
        except PageNotAnInteger:
            visible_films = paginator.page(1)
        except EmptyPage:
            visible_films = paginator.page(paginator.num_pages)

        context['order_by'] = order_by
        context['direction'] = direction
        context['visible_films'] = visible_films
        context['genre'] = self.kwargs['genre'].capitalize()
        return context


class Top100View(ListView):
    model = Film
    context_object_name = 'top100'

    def get_queryset(self):
        return Film.objects.all().order_by('-score')[:100]

    template_name = 'films/top100.html'


def pages(request):
    order_by = request.GET.get('order_by')
    page = request.GET.get('page')
    direction = request.GET.get('direction')
    ordering = order_by.lower()
    if direction == 'desc':
        ordering = '-{}'.format(ordering)
    films = Film.objects.all().order_by(ordering)
    paginator = Paginator(films, 60)
    try:
        visible_films = paginator.page(page)
    except PageNotAnInteger:
        visible_films = paginator.page(1)
    except EmptyPage:
        visible_films = paginator.page(paginator.num_pages)
    return render(request, 'films/all_films.html',
                  {'visible_films': visible_films,
                   'order_by': order_by, 'direction': direction})


def search_bar(request):
    if request.method == "GET":
        search = request.GET.get("q")
        results = Film.objects.all().filter(Q(title__icontains=search) |
                                  Q(director__icontains=search) |
                                  Q(actors__icontains=search) |
                                  Q(country__icontains=search))
        return render(request, 'films/search_bar.html', {'results': results, 'search': search})

def minigame(request):
    films = list(Film.objects.all())
    rand_film = random.choice(films)
    rand_title = rand_film.title
    rand_film_joined = rand_title.replace(" ", "")
    print(rand_film)
    print(rand_film.title)
    while any(not c.isalnum() for c in rand_film_joined):
        rand_film = random.choice(films)
        rand_title = rand_film.title
        rand_film_joined = rand_title.replace(" ", "")
        print(rand_film)
    return render(request, 'films/minigame.html', {'random_film': rand_film})


@login_required(login_url='login')
def rated(request, film_id):
    if request.method == "POST":
        try:
            reviews = Comment.objects.get(user__id=request.user.id, film__id=film_id)
            rating = reviews.rating
            delete_rating = (reviews.film.score * reviews.film.votes - rating)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            update_rating = (delete_rating + reviews.rating) / reviews.film.votes
            reviews.film.score = update_rating
            reviews.film.save()
            messages.success(request, "Thank you! Your review has been updated!")
            return redirect("films:detail", pk=film_id)
        except Comment.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.subject = form.cleaned_data['subject']
                data.comment = form.cleaned_data['comment']
                data.rating = form.cleaned_data['rating']
                data.film_id = film_id
                data.user_id = request.user.id
                data.film.score = (data.film.score * data.film.votes + data.rating) / (data.film.votes + 1)
                data.film.votes += 1
                data.save()
                data.film.save()
                messages.success(request, "Thank you! Your review has been added!")
                return redirect('films:detail', pk=film_id)
