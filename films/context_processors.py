from .models import Film


def genres(request):
    genres_list = Film.objects.values_list('genre', flat=True)
    all_genres = []
    for elem in genres_list:
        splited = elem.split(", ")
        for genre in splited:
            all_genres.append(genre)
    all_genres = sorted(set(all_genres))
    return {'all_genres': all_genres}