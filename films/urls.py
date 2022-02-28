from django.urls import path, re_path
from . import views


app_name = "films"

urlpatterns = [
    # /films/
    # re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    # /films/film/<id>/
    re_path(r'^film/(?P<pk>[0-9]+)/$', views.Detail_view.as_view(), name='detail'),
    # /films/film/<id>/rated/
    path('submit_review/<int:film_id>', views.rated, name='rated'),
    # /films/page=<page>/
    re_path(r'^allfilms/\w{0,100}$', views.pages, name='pages'),
    re_path(r'^hangman/$', views.minigame, name='minigame'),
    re_path(r'^search/$', views.search_bar, name='search'),
    # /films/top_100/
    re_path(r'^top100/$', views.Top100View.as_view(), name='top_100'),
    # /films/<genre>/
    # re_path(r'^(?P<genre>)/&', views.genre, name='genre'),
    re_path(r'^(?P<genre>[\w\-]+)/\w{0,100}$', views.GenreListView.as_view(), name='genre'),
    re_path(r'^$', views.IndexView.as_view(), name='index'),

]
