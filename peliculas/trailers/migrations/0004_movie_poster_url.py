# Generated by Django 5.0.7 on 2024-07-29 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailers', '0003_alter_trailer_trailer_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
