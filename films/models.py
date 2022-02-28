from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class Film(models.Model):
    title = models.CharField(_("title"), max_length=150, default=None)
    release_date = models.IntegerField(_("year"), default=None)
    genre = models.CharField(_("genre"), max_length=200, default=None)  # musi byc oddzielne przegladnie po rodzajach
    duration = models.IntegerField(_("duration"), default=None)
    country = models.CharField(_("country"), max_length=50, default=None)
    director = models.CharField(_("director"), max_length=70, default=None)  # oceny dla rezyserów??
    actors = models.CharField(_("actors"), max_length=1000, default=None)
    score = models.DecimalField(_("avg_vote"), decimal_places=3, max_digits=4, default=None)
    votes = models.IntegerField(_("votes"), default=None)
    poster = models.URLField(_("poster"), max_length=2000, default=None)
    # rated = models.IntegerField(default=None)

    def __str__(self):
        return f'{self.title} ({self.release_date})'


class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField()
    add_t = models.DateTimeField(auto_now_add=True)
    edit_t = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
