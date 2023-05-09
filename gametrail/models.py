from datetime import datetime, timedelta
from datetime import date
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as userDjango
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils.timezone import now as currentDate
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
    def create_superuser(self, email, userName, avatar, password):
        user = self.create_user(
            email = self.normalize_email(email),
            userName = userName,
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
    
    def create_user(self, userName, email, avatar,password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        if not userName:
            raise ValueError('El usuario debe tener un nombre de usuario')

        userDjango = userDjango()
        userDjango.userName = userName
        userDjango.set_password(password)
        userDjango.save()
        userDjango.is_active = True

        userName_gameTrail = userName

        user = self.model(
            email=self.normalize_email(email),
            userName=userName_gameTrail,
            avatar=avatar,
        )

        user.set_password(password)
        user.save()

        gameList = GameList()
        gameList.user = user
        gameList.save()

        return user

class User(AbstractBaseUser):

    userName = models.CharField(max_length=400, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.URLField(max_length=255)
    password = models.CharField(max_length=500)
    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=STANDARD,
    )
    suscription_time = models.DateField(default=datetime(2023, 1, 1), null=True, blank=True)
    last_login = None
    is_active = models.BooleanField(default=False)

    userName_FIELD = 'userName'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    
    def is_subscription_expired(self):
        if self.plan == PREMIUM and self.suscription_time:
            tiempo = datetime.now().date() - self.suscription_time
            if tiempo >= timedelta(days=30):
                self.plan = STANDARD
                self.suscription_time = None
                self.save()
                return True
        return False

    def __str__(self):
        return f'{self.userName}'
    
    @property
    def average_ratings(self):
        ratings = Rating.objects.filter(ratedUser_id = self.id)
        if not ratings:
            return []
        types = ["KINDNESS", "FUNNY", "TEAMWORK", "ABILITY", "AVAILABILITY"]
        res = dict()
        res["ratedUser"] = self.id
        for type in types:
            avg_rating = Rating.objects.filter(ratedUser_id = self.id, type = type).aggregate(Avg('rating'))['rating__avg']
            res[type] = avg_rating
        return res

class Rating(models.Model):
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    type = models.CharField(max_length=255,choices=TYPE_CHOICES)
    ratedUser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rate_recieved')
    userWhoRate = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rate_made')
    
    class Meta:
            unique_together = ('type', 'ratedUser','userWhoRate')
    
    

    def __str__(self):
        return f'{self.userWhoRate.userName} rated {self.ratedUser.userName} with {self.rating} for {self.type}'
    
class GameList(models.Model):

    user = models.OneToOneField('User',on_delete=models.CASCADE, unique=True, related_name='gameList')
    
    def __str__(self):
        return f'{self.user.userName}\'s game list'
    
class Game(models.Model):

    name = models.CharField(max_length=1000)
    releaseDate = models.DateField(null=True, blank=True)
    image = models.URLField(max_length=1000, null=True, blank=True)
    photos = models.CharField(max_length=2000, null=True, blank=True)
    description = models.TextField(default='Lorem Ipsum')

    def __str__(self):
        return self.name

class Comment(models.Model):
    commentText = models.TextField(max_length=350)
    userWhoComments = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    userCommented = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments_received')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True, related_name = "comments_games")
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
    game = models.ManyToManyField(Game, related_name="genres")

    def __str__(self):
        return self.genre

class Trail(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    startDate = models.DateField()
    finishDate = models.DateField()
    maxPlayers = models.IntegerField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateField(default=currentDate, null=True, blank=True)

    def clean(self):
        if self.finishDate < self.startDate:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio!')
        
        elif self.startDate < date.today():
            raise ValidationError('La fecha de inicio no puede ser un dia que ya ha pasado!')
    
        return super().clean()

    def __str__(self):
        
        return self.name
    
    @property
    def average_ratings(self):
        res=0
        if self.users.count() == 0:
            return 0
        for user in self.users.all():
            avgRatings= user.user.average_ratings
            if len(avgRatings):
                avgRatings.pop("ratedUser")
                res+= sum(value for value in avgRatings.values() if value is not None)/len(avgRatings.values())
        res=res/self.users.count()
        return res
    
class UserInTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trails_with_user')
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE,related_name='users')

    class Meta:
        unique_together = ('user', 'trail',)

    def clean(self) :
        numJugadoresTrail=self.trail.users.count()
        if numJugadoresTrail >= self.trail.maxPlayers:
            raise ValidationError('El número de Usuarios del Trail no puede superar el número máximo de jugadores!')
        return super().clean()

    def __str__(self):
        return f"{self.user.userName} in {self.trail.name}"
    
class GameInTrail(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE,related_name='trails')
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE,related_name='games')
    message = models.TextField()
    priority = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('game', 'trail')

    def clean(self) :
        if self.priority > 5:
            raise ValidationError('La prioridad debe ser inferior o igual a 5!')
        return super().clean()

    def __str__(self):
        return f"{self.game.name} in {self.trail.name}"
    
class Platform(models.Model):
    platform = models.CharField(max_length=500)
    game = models.ManyToManyField(Game, related_name="platforms")
    trail = models.ManyToManyField(Trail,related_name='platforms')

    def __str__(self):
        return self.platform
    
class ChatTrail(models.Model):
    chatText = models.TextField()
    createdMoment = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.userName} - {self.chatText}"
    
class SabiasQue(models.Model):
    curiosity = models.TextField()

    def __str__(self):
        return self.curiosity
    
class MinRatingTrail(models.Model):
    
    minRating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trail = models.ForeignKey(Trail, on_delete=models.SET_NULL, null=True, blank=True)
    ratingType = models.CharField(max_length=50, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('trail', 'ratingType')

    def __str__(self):
        return f"{self.ratingType} - {self.minRating}"


class TrailPatrocinado(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE,related_name='trail')

    def __str__(self):
        return self.trail