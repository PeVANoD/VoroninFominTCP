from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  render,redirect, get_object_or_404
from .models import  Tag, Painting, Artist
from django.db.models import Prefetch
from django.core.paginator import Paginator
@csrf_exempt
def paintingsList(request):
    paintings = Painting.objects.all()
    return render(request,'art/paintingsList.html',{'paintings':paintings})
@csrf_exempt
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
@csrf_exempt
def home(request):
    return render(request, 'art/home.html')
@csrf_exempt
def artists(request):
    all_artists = Artist.objects.all()
    selected_artist_id = None
    paintings = None

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

#CRUD
@csrf_exempt
def manage_content(request):
    # Получаем все данные для отображения
    context = {
        'tags': Tag.objects.all(),
        'artists': Artist.objects.all(),
        'paintings': Painting.objects.all().prefetch_related('artist', 'tags')
    }
    
    # Обработка POST запросов (CRUD операции)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Обработка тегов
        if action == 'create_tag':
            Tag.objects.create(name=request.POST.get('tag_name'))
        elif action == 'update_tag':
            tag = Tag.objects.get(id=request.POST.get('tag_id'))
            tag.name = request.POST.get('tag_name')
            tag.save()
        elif action == 'delete_tag':
            Tag.objects.get(id=request.POST.get('tag_id')).delete()
        
        # Обработка художников
        elif action == 'create_artist':
            Artist.objects.create(
                name=request.POST.get('artist_name'),
                biography=request.POST.get('biography'),
                photoURL=request.POST.get('photo_url')
            )
        elif action == 'update_artist':
            artist = Artist.objects.get(id=request.POST.get('artist_id'))
            artist.name = request.POST.get('artist_name')
            artist.biography = request.POST.get('biography')
            artist.photoURL = request.POST.get('photo_url')
            artist.save()
        elif action == 'delete_artist':
            Artist.objects.get(id=request.POST.get('artist_id')).delete()
        
        # Обработка картин
        elif action == 'create_painting':
            painting = Painting.objects.create(
                title=request.POST.get('title'),
                imageURL=request.POST.get('image_url'),
                description=request.POST.get('description', '')
            )
            painting.artist.set(request.POST.getlist('artists'))
            painting.tags.set(request.POST.getlist('tags'))
        elif action == 'update_painting':
            painting = Painting.objects.get(id=request.POST.get('painting_id'))
            painting.title = request.POST.get('title')
            painting.imageURL = request.POST.get('image_url')
            painting.description = request.POST.get('description', '')
            painting.save()
            painting.artist.set(request.POST.getlist('artists'))
            painting.tags.set(request.POST.getlist('tags'))
        elif action == 'delete_painting':
            Painting.objects.get(id=request.POST.get('painting_id')).delete()
        
        return redirect('manage_content')  # Редирект после POST
    
    return render(request, 'art/manage_content.html', context)

