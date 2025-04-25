from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  render,redirect, get_object_or_404
from .models import  Tag, Painting, Artist
from django.db.models import Prefetch
from django.core.paginator import Paginator

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from .serializers import RegisterSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer

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

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
User = get_user_model()
@csrf_exempt
def artists(request):
    # Получаем всех пользователей с пометкой is_artist=True
    artist_users = User.objects.filter(is_artist=True).select_related('artist')
    selected_username = request.GET.get('username')
    paintings = None

    if selected_username:
        try:
            artist_user = artist_users.get(username=selected_username)
            paintings = Painting.objects.filter(artist=artist_user.artist)
        except User.DoesNotExist:
            paintings = Painting.objects.none()
    else:
        paintings = Painting.objects.none()

    return render(request, 'art/artists.html', {
        'paintings': paintings,
        'artist_users': artist_users,
        'selected_username': selected_username
    })
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework import status
from django.contrib.auth.decorators import login_required

def auth_page(request):
    return render(request, 'art/auth.html')

@require_http_methods(["GET"])
def auth_page(request):
    return render(request, 'art/auth.html')

#CRUD
@csrf_exempt
@api_view(['GET', 'POST'])
def manage_content(request): #проверяем залогинен ли польховатль и тогда перекидываем.
    if isinstance(request.user, AnonymousUser):
        paintings = Painting.objects.all()
        return render(request, 'art/guest_page.html', {
            'paintings': paintings
        })
    
    # Остальной код для авторизованных пользователей
    context = {
        'tags': Tag.objects.all(),
        'artists': Artist.objects.all(),
        'paintings': Painting.objects.all().prefetch_related('artist', 'tags')
    }
    
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
        
        return redirect('manage_content')
    
    return render(request, 'art/manage_content.html', context)


#JWT


def guest_page(request):
    paintings = Painting.objects.all()
    return render(request, 'art/guest_page.html', {
        'paintings': paintings
    })
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')  # Перенаправляем на страницу входа

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Замените 'home' на нужный URL
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'registration/custom_login.html')

from .forms import CustomUserCreationForm  # Add this import

def custom_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = form.cleaned_data.get('is_artist', False)
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/custom_register.html', {'form': form})

from .forms import ArtistProfileForm, PaintingForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
@login_required
def artist_dashboard(request):
    if not request.user.is_artist:
        return redirect('home')
    
    artist = get_object_or_404(Artist, user=request.user)
    all_tags = Tag.objects.all()
    
    # Handle profile form
    if request.method == 'POST' and 'profile_form' in request.POST:
        profile_form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('artist_dashboard')
    else:
        profile_form = ArtistProfileForm(instance=artist)
    
    # Handle tag operations
    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'create_tag':
            tag_name = request.POST.get('tag_name')
            if tag_name:
                Tag.objects.get_or_create(name=tag_name)
                return redirect('artist_dashboard')
        
        elif request.POST['action'] == 'update_tag':
            tag_id = request.POST.get('tag_id')
            tag_name = request.POST.get('tag_name')
            if tag_id and tag_name:
                tag = get_object_or_404(Tag, id=tag_id)
                tag.name = tag_name
                tag.save()
                return redirect('artist_dashboard')
        
        elif request.POST['action'] == 'delete_painting':
            painting_id = request.POST.get('painting_id')
            if painting_id:
                painting = get_object_or_404(Painting, id=painting_id, artist=artist)
                painting.delete()
                return redirect('artist_dashboard')
    
    # Handle painting form
    if request.method == 'POST' and 'painting_form' in request.POST:
        painting_id = request.POST.get('painting_id')
        
        if painting_id:  # Editing existing painting
            painting = get_object_or_404(Painting, id=painting_id, artist=artist)
            painting_form = PaintingForm(request.POST, request.FILES, instance=painting)
        else:  # Creating new painting
            painting_form = PaintingForm(request.POST, request.FILES)
        
        if painting_form.is_valid():
            painting = painting_form.save(commit=False)
            painting.artist = artist
            if 'image' in request.FILES:
                painting.image = request.FILES['image']
            painting.save()
            painting_form.save_m2m()  # For tags
            return redirect('artist_dashboard')
    else:
        painting_form = PaintingForm()
    
    # Get all artist's paintings
    paintings = Painting.objects.filter(artist=artist).order_by('-created_at')
    
    return render(request, 'artist/dashboard.html', {
        'artist': artist,
        'profile_form': profile_form,
        'painting_form': painting_form,
        'paintings': paintings,
        'all_tags': all_tags,
    })