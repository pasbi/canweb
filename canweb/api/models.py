from django.db import models

# Create your models here.

class Song(models.Model):
    label = models.TextField(blank=True)
    pattern = models.TextField()

    def __str__(self):
        return self.label

