# Generated by Django 5.0.1 on 2024-01-31 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0008_alter_genre_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customarticles',
            old_name='genre_id',
            new_name='genre',
        ),
    ]
