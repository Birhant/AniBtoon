# Generated by Django 3.0 on 2021-12-27 10:07

import Films.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Films', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='relation',
            new_name='Contents',
        ),
        migrations.AddField(
            model_name='film',
            name='episode',
            field=models.IntegerField(default=0, null=True, validators=[Films.models.valid_episode]),
        ),
        migrations.AlterField(
            model_name='film',
            name='alternative_title',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='film',
            name='profile_pic',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='film',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[Films.models.valid_rating]),
        ),
    ]
