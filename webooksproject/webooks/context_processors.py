from .models import Genre

def genres(request):
    genres = Genre.objects.all().order_by('name')

    return {'genres': genres}
