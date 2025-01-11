from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks')
    image_url = models.URLField()
    def __str__(self):
        return self.title
