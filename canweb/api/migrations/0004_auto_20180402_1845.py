# Generated by Django 2.0.3 on 2018-04-02 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180401_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='midiCommand',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='spotifyTrackId',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='youtubeTrackId',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='label',
            field=models.TextField(blank=True),
        ),
    ]