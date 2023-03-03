from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=100)
    img = models.CharField(max_length=300)
    def __str__(self):
        return self.title