# Generated by Django 4.1.6 on 2023-03-07 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gametrail', '0004_remove_genre_game_remove_platform_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='game',
            field=models.ManyToManyField(to='gametrail.game'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='trail',
            field=models.ManyToManyField(to='gametrail.trail'),
        ),
    ]
