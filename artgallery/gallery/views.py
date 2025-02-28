from rest_framework import viewsets
from .models import Artist, Tag, Painting
from .serializers import ArtistSerializer, TagSerializer, PaintingSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PaintingViewSet(viewsets.ModelViewSet):
    queryset = Painting.objects.all()
    serializer_class = PaintingSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.request.query_params.get('tag')
        artist_id = self.request.query_params.get('artist')
        
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)
            
        return queryset
