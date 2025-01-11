from django.shortcuts import render, get_object_or_404
from .models import Artist, Artwork

def index(request):
    return render(request, 'gallery/index.html', {'artists': Artist.objects.all()})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return render(request, 'gallery/artist_detail.html', {'artist': artist})

def artist_gallery(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    artworks = artist.artworks.all()
    return render(request, 'gallery/artist_gallery.html', {'artist': artist, 'artworks': artworks})
