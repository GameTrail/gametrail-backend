from django.db import models
from django.utils import timezone


#Enum declarations

PLAYING = 'PLAYING'
PENDING = 'PENDING'
FINISHED = 'FINISHED'

STATUS_CHOICES = [
    (PLAYING, 'Playing'),
    (PENDING, 'Pending'),
    (FINISHED, 'Finished'),
]

PREMIUM = 'PREMIUM'
STANDARD = 'STANDARD'

PLAN_CHOICES = [
    (PREMIUM, 'Premium'),
    (STANDARD, 'Standard'),
]

KINDNESS = 'KINDNESS'
FUNNY = 'FUNNY'
TEAMWORK = 'TEAMWORK'
ABILITY = 'ABILITY'
AVAILABILITY = 'AVAILABILITY'

TYPE_CHOICES = [
    (KINDNESS, 'Kindness'),
    (FUNNY, 'Funny'),
    (TEAMWORK, 'Teamwork'),
    (ABILITY, 'Ability'),
    (AVAILABILITY, 'Availability'),
]

# Create your models here.
class User(models.Model):
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField()
    password = models.CharField()

    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=STANDARD,
    )

    def __str__(self):
        return self.username

class Rating(models.Model):
    
    rating = models.IntegerField()
    type = models.CharField(choices=TYPE_CHOICES)
    ratedUser = models.ForeignKey('User', on_delete=models.CASCADE)
    userWhoRate = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userWhoRate.username} rated {self.ratedUser.username} with {self.rating} for {self.type}'
    
class GameList(models.Model):

    user = models.OneToOneField('User',on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}\'s game list'
    
class Game(models.Model):

    name = models.CharField(max_length=100)
    releaseDate = models.DateField()
    image = models.CharField()
    photos = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    commentText = models.TextField()
    userWhoComments = models.ForeignKey(User, on_delete=models.CASCADE)
    userCommented = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.commentText
    
class GameInList(models.Model):
    creationMoment = models.DateTimeField(default=timezone.now)
    lastModified = models.DateTimeField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gameList = models.ForeignKey(GameList, on_delete=models.CASCADE, related_name='games_in_list')
    status = models.CharField(choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.game} in {self.gameList} ({self.status})"
    
class Genre(models.Model):
    genre = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='genres')

    def __str__(self):
        return self.genre

class Trail(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    startDate = models.DateField()
    finishDate = models.DateField()
    maxPlayers = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name   
    
class UserInTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.trail.name}"
    
class Platform(models.Model):
    platform = models.CharField(max_length=40)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.platform
    
class ChatTrail(models.Model):
    chatText = models.TextField()
    createdMoment = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.chatText}"
    
class SabiasQue(models.Model):
    curiosity = models.TextField()

    def __str__(self):
        return self.curiosity
    
class MinRatingTrail(models.Model):
    
    minRating = models.IntegerField()
    trail = models.ForeignKey(Trail, on_delete=models.SET_NULL, null=True, blank=True)
    ratingType = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.ratingType} - {self.minRating}"