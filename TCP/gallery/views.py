
from django.shortcuts import  render,redirect, get_object_or_404
from .models import  Tag, Painting, Artist
from django.db.models import Prefetch

def paintingsList(request):
    paintings = Painting.objects.all()
    return render(request,'art/paintingsList.html',{'paintings':paintings})

def tagSearch(request):
    tag_name = request.GET.get('tag')  # Получаем параметр тега из запроса
    if tag_name:
        paintings = Painting.objects.filter(tags__name=tag_name)  # Фильтруем картины по тегу
    else:
        paintings = Painting.objects.all()  # Если тег не выбран, показываем все картины
    
    tags = Tag.objects.all()  # Получаем все теги для отображения в списке
    
    return render(request, 'art/tagSearch.html', {
        'paintings': paintings,
        'tags': tags,
        'selected_tag': tag_name
    })

def home(request):
    return render(request, 'art/home.html')

def artists(request):
    all_artists = Artist.objects.all()
    selected_artist_id = request.GET.get('artist_id')

    if selected_artist_id:
        selected_artist = Artist.objects.filter(id=selected_artist_id).prefetch_related(
            Prefetch('artists', queryset=Painting.objects.all())
        ).first()

        paintings = selected_artist.artists.all() if selected_artist else Painting.objects.none()
    else:
        selected_artist = None
        paintings = Painting.objects.none()

    return render(request, 'art/artists.html', {
        'paintings': paintings,
        'artists': all_artists,
        'selected_artist': selected_artist
    })