# Generated by Django 4.1.6 on 2023-04-08 17:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('releaseDate', models.DateField(blank=True, null=True)),
                ('image', models.URLField(blank=True, max_length=1000, null=True)),
                ('photos', models.CharField(blank=True, max_length=2000, null=True)),
                ('description', models.TextField(default='Lorem Ipsum')),
            ],
        ),
        migrations.CreateModel(
            name='SabiasQue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curiosity', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=400, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('avatar', models.URLField(max_length=255)),
                ('password', models.CharField(max_length=500)),
                ('plan', models.CharField(choices=[('PREMIUM', 'Premium'), ('STANDARD', 'Standard')], default='STANDARD', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('startDate', models.DateField()),
                ('finishDate', models.DateField()),
                ('maxPlayers', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gametrail.user')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=500)),
                ('game', models.ManyToManyField(related_name='platforms', to='gametrail.game')),
                ('trail', models.ManyToManyField(related_name='platforms', to='gametrail.trail')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=500)),
                ('game', models.ManyToManyField(related_name='genres', to='gametrail.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gameList', to='gametrail.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField(max_length=350)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_games', to='gametrail.game')),
                ('userCommented', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_received', to='gametrail.user')),
                ('userWhoComments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_made', to='gametrail.user')),
            ],
        ),
        migrations.CreateModel(
            name='ChatTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatText', models.TextField()),
                ('createdMoment', models.DateTimeField(default=django.utils.timezone.now)),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gametrail.trail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gametrail.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserInTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='gametrail.trail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trails_with_user', to='gametrail.user')),
            ],
            options={
                'unique_together': {('user', 'trail')},
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('type', models.CharField(choices=[('KINDNESS', 'Kindness'), ('FUNNY', 'Funny'), ('TEAMWORK', 'Teamwork'), ('ABILITY', 'Ability'), ('AVAILABILITY', 'Availability')], max_length=255)),
                ('ratedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_recieved', to='gametrail.user')),
                ('userWhoRate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_made', to='gametrail.user')),
            ],
            options={
                'unique_together': {('type', 'ratedUser', 'userWhoRate')},
            },
        ),
        migrations.CreateModel(
            name='MinRatingTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minRating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('ratingType', models.CharField(choices=[('KINDNESS', 'Kindness'), ('FUNNY', 'Funny'), ('TEAMWORK', 'Teamwork'), ('ABILITY', 'Ability'), ('AVAILABILITY', 'Availability')], max_length=50)),
                ('trail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gametrail.trail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gametrail.user')),
            ],
            options={
                'unique_together': {('trail', 'ratingType')},
            },
        ),
        migrations.CreateModel(
            name='GameInTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('priority', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(choices=[('PLAYING', 'Playing'), ('PENDING', 'Pending'), ('FINISHED', 'Finished')], max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trails', to='gametrail.game')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='gametrail.trail')),
            ],
            options={
                'unique_together': {('game', 'trail')},
            },
        ),
        migrations.CreateModel(
            name='GameInList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationMoment', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastModified', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('PLAYING', 'Playing'), ('PENDING', 'Pending'), ('FINISHED', 'Finished')], max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gametrail.game')),
                ('gameList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_in_list', to='gametrail.gamelist')),
            ],
            options={
                'unique_together': {('game', 'gameList')},
            },
        ),
    ]
