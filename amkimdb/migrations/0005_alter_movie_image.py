# Generated by Django 4.0.3 on 2022-03-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amkimdb', '0004_alter_movie_released_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_pics'),
        ),
    ]