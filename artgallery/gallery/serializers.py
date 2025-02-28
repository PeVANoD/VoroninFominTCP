from rest_framework import serializers
from .models import Artist, Painting, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'biography', 'photo', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PaintingSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        source='artist',
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        many=True,
        required=False
    )
    
    class Meta:
        model = Painting
        fields = ['id', 'title', 'imageURL', 'description', 'artist', 'artist_id', 'tags', 'tag_ids']
