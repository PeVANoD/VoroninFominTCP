
from django.shortcuts import  render,redirect
from .models import  Tag, Painting

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