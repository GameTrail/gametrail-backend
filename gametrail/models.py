from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    photos = models.CharField(max_length=400)
    departureDate = models.DateField(null = True)
    
    ND='No definido'
    ACTION='ACTION'
    SPORT='SPORT'
    ROL='ROL'

    TYPE= (
        (ND,'No definido'),
        (ACTION,'ACTION'),
        (SPORT,'SPORT'),
        (ROL,'ROL'),
        )

    genres = models.CharField(
            max_length=255,
            choices=TYPE,
            default=ND)

    XBOX='XBOX'
    PLAYSTATION='PLAYSTATION'
    PC='PC'

    PLATFORMTYPES= (
        (ND,'No definido'),
        (XBOX,'XBOX'),
        (PLAYSTATION,'PLAYSTATION'),
        (PC,'PC'),
        )

    platform = models.CharField(
            max_length=255,
            choices=PLATFORMTYPES,
            default=ND)
    def __str__(self):
        return self.title

class User(models.Model):
    nameUser = models.CharField(max_length=100)
    email = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    STANDARD='STANDARD'
    PREMIUM='PREMIUM'

    PLANTYPES= (
        (STANDARD,'STANDARD'),
        (PREMIUM,'PREMIUM'),
        )

    plan = models.CharField(
            max_length=255,
            choices=PLANTYPES,
            default=STANDARD)
