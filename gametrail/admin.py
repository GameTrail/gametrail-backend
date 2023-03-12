from django.contrib import admin
from gametrail.models import GameInTrail
from gametrail.models import User
from gametrail.models import Trail
from gametrail.models import Game


# Register your models here.

admin.site.register(Trail)
admin.site.register(GameInTrail)
admin.site.register(User)
admin.site.register(Game)