from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as UserDjango
from django.core.exceptions import ValidationError

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

class UserManager(BaseUserManager):
    def create_superuser(self, email, username, avatar, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            avatar = avatar
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_authenticated = True
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, avatar,password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')

        userDjango = UserDjango()
        userDjango.username = username
        userDjango.set_password(password)
        userDjango.save()
        userDjango.is_active = True

        username_gameTrail = username

        user = self.model(
            email=self.normalize_email(email),
            username=username_gameTrail,
            avatar=avatar,
        )

        user.set_password(password)
        user.save()

        gameList = GameList()
        gameList.user = user
        gameList.save()
        
        return user

class User(AbstractBaseUser):

    username = models.CharField(max_length=400, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.URLField(max_length=255)
    password = models.CharField(max_length=500)
    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=STANDARD,
    )

    last_login = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return f'{self.username}'

class Rating(models.Model):
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    type = models.CharField(max_length=255,choices=TYPE_CHOICES)
    ratedUser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rate_recieved')
    userWhoRate = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rate_made')

    def __str__(self):
        return f'{self.userWhoRate.username} rated {self.ratedUser.username} with {self.rating} for {self.type}'
    
class GameList(models.Model):

    user = models.OneToOneField('User',on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return f'{self.user.username}\'s game list'
    
class Game(models.Model):

    name = models.CharField(max_length=1000)
    releaseDate = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=1000, null=True, blank=True)
    photos = models.CharField(max_length=2000, null=True, blank=True)
    description = models.TextField(default='Lorem Ipsum')

    def __str__(self):
        return self.name

class Comment(models.Model):
    commentText = models.TextField()
    userWhoComments = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    userCommented = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments_received')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.commentText
    
class GameInList(models.Model):
    creationMoment = models.DateTimeField(default=timezone.now)
    lastModified = models.DateTimeField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gameList = models.ForeignKey(GameList, on_delete=models.CASCADE, related_name='games_in_list')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('game', 'gameList',)

    def __str__(self):
        return f"{self.game} in {self.gameList} ({self.status})"

    def clean(self):
        if self.creationMoment > self.lastModified:
            raise ValidationError('The modified date can not before creation date.')
    
class Genre(models.Model):
    genre = models.CharField(max_length=500)
    game = models.ManyToManyField(Game)

    def __str__(self):
        return self.genre

class Trail(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    startDate = models.DateField()
    finishDate = models.DateField()
    maxPlayers = models.IntegerField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name   
    
class UserInTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'trail',)

    def __str__(self):
        return f"{self.user.username} in {self.trail.name}"
    
class GameInTrail(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    message = models.TextField()
    priority = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('game', 'trail',)

    def __str__(self):
        return f"{self.game.name} in {self.trail.name}"
    
class Platform(models.Model):
    platform = models.CharField(max_length=500)
    game = models.ManyToManyField(Game)
    trail = models.ManyToManyField(Trail)

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
    
    minRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trail = models.ForeignKey(Trail, on_delete=models.SET_NULL, null=True, blank=True)
    ratingType = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.ratingType} - {self.minRating}"
