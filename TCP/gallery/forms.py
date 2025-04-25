from django import forms
from .models import Artist, Painting, Tag

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['biography', 'photoURL']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4}),
        }

class PaintingForm(forms.ModelForm):
    class Meta:
        model = Painting
        fields = ['title', 'description', 'image', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        
    def save(self, commit=True):
        painting = super().save(commit=False)
        if commit:
            painting.save()
            tags = self.cleaned_data['tags']
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                for tag_name in tag_list:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    painting.tags.add(tag)
        return painting

from django.contrib.auth.forms import UserCreationForm
from .models import User
class CustomUserCreationForm(UserCreationForm):
    is_artist = forms.BooleanField(
        required=False,
        label='Are you an artist?',
        help_text='Check this if you want to register as an artist'
    )
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_artist')

class ArtistRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_artist = True  # Помечаем как артиста
        if commit:
            user.save()  # Это вызовет сигнал post_save и создаст Artist
        return user