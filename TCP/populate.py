import os
import django
from faker import Faker

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artgallery.settings')
django.setup()

from gallery.models import Tag, Artist, Painting

fake = Faker()

def create_tags(n):
    for _ in range(n):
        Tag.objects.create(name=fake.word())

def create_artists(n):
    for _ in range(n):
        Artist.objects.create(
            name=fake.name(),
            biography=fake.text(),
            photoURL=fake.image_url()
        )

def create_paintings(n):
    tags = list(Tag.objects.all())
    artists = list(Artist.objects.all())
    
    for _ in range(n):
        painting = Painting.objects.create(
            title=fake.sentence(),
            imageURL=fake.image_url(),
            description=fake.text()
        )
        
        # Добавляем случайные теги и художников
        painting.tags.set(fake.random_elements(elements=tags, length=fake.random_int(min=1, max=5)))
        painting.artist.set(fake.random_elements(elements=artists, length=fake.random_int(min=1, max=3)))

if __name__ == '__main__':
    paints = Painting.objects.all()
    if paints == 0:
        create_tags(10)
        create_artists(5)
        create_paintings(20)
        print("База данных успешно заполнена!")
    else:
        print("База данных не пустая!")