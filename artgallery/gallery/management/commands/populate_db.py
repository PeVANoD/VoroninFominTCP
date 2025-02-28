from django.core.management.base import BaseCommand
from gallery.models import Artist, Tag, Painting
from django.utils.crypto import get_random_string
import random


class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        # Создание тегов
        tags = []
        tag_names = ['Импрессионизм', 'Абстрактное', 'Портрет', 'Пейзаж', 'Модерн', 
                    'Классицизм', 'Реализм', 'Сюрреализм', 'Экспрессионизм', 'Кубизм']
        
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')
        # Создание художников
        artists = []
        artist_data = [
            {
                'name': 'Иван Иванов',
                'email': 'ivan@example.com',
                'biography': 'Известный российский художник, специализирующийся на пейзажах.'
            },
            {
                'name': 'Анна Петрова',
                'email': 'anna@example.com',
                'biography': 'Мастер портретной живописи с современным подходом.'
            },
            {
                'name': 'Сергей Сидоров',
                'email': 'sergey@example.com',
                'biography': 'Абстракционист, известный своими яркими работами.'
            }
        ]
        
        for data in artist_data:
            artist, created = Artist.objects.get_or_create(
                email=data['email'],
                defaults={
                    'name': data['name'],
                    'biography': data['biography']
                }
            )
            
            if created:
                artist.set_password('password123')
                artist.save()
                self.stdout.write(f'Created artist: {data["name"]}')
            
            artists.append(artist)
        
        # Создание картин
        painting_data = [
            {
                'title': 'Закат на реке',
                'imageURL': 'https://example.com/sunset.jpg',
                'description': 'Пейзаж заката над рекой в тёплых тонах.',
                'artist': artists[0],
                'tags': [tags[0], tags[3]]
            },
            {
                'title': 'Портрет незнакомки',
                'imageURL': 'https://example.com/portrait.jpg',
                'description': 'Портрет женщины в классическом стиле.',
                'artist': artists[1],
                'tags': [tags[2], tags[5]]
            },
            {
                'title': 'Абстрактная композиция №5',
                'imageURL': 'https://example.com/abstract.jpg',
                'description': 'Абстрактная композиция в ярких цветах.',
                'artist': artists[2],
                'tags': [tags[1], tags[7]]
            },
            {
                'title': 'Городской пейзаж',
                'imageURL': 'https://example.com/city.jpg',
                'description': 'Современный городской пейзаж в вечернее время.',
                'artist': artists[0],
                'tags': [tags[3], tags[6]]
            },
            {
                'title': 'Мечты',
                'imageURL': 'https://example.com/dreams.jpg',
                'description': 'Сюрреалистическая композиция, отражающая внутренний мир художника.',
                'artist': artists[2],
                'tags': [tags[7], tags[8]]
            }
        ]
        
        for data in painting_data:
            painting, created = Painting.objects.get_or_create(
                title=data['title'],
                imageURL=data['imageURL'],
                defaults={
                    'description': data['description'],
                    'artist': data['artist']
                }
            )
            
            if created:
                painting.tags.set(data['tags'])
                self.stdout.write(f'Created painting: {data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Database population completed!'))
