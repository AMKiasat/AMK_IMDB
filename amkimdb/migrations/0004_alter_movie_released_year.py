# Generated by Django 4.0.3 on 2022-03-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amkimdb', '0003_comment_movie_delete_post_comment_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='released_year',
            field=models.CharField(max_length=10),
        ),
    ]
