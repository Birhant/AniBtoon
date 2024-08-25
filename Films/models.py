from django.db import models
from django.forms import ValidationError

def valid_rating(value):
    if value>=0 and value<=10.00:
        return value
    else:
        raise ValidationError('please enter 0 to 10.00')

def valid_episode(value):
    if value>=0:
        return value
    else:
        raise ValidationError('Enter non negative number')

# Create your models here.
class Film(models.Model):
    category_choices = (
        ('anime',"Anime"),
        ('cartoon', "Cartoon"),
        ('manga', "Manga"),
        ('comic', "Comic"),
        ('live action', 'Live action')
    )
    Contents_choices = (
        ('original', "Original"),
        ('series', "Series"),
        ('movie', "Movie"),
        ('alternative', "Alternative"),
        ('ova', "OVA"),
        ('new', "new"),
        ('fds', "fdf"),
    )
    status_choices = (
        ('ONGOING', "ONGOING"),
        ('UPCOMING', "UPCOMING"),
        ('FINISHED', "FINISHED"),
        ('PLANNED', "PLANNED"),
        ('HELLO', "HELLO"),
        ('WELCOME', "WELCOME"),
    )
    title = models.CharField(max_length = 200, unique=True)
    alternative_title = models.TextField(default="")
    category = models.CharField(max_length = 100, choices = category_choices, default = category_choices[0][0])
    production = models.CharField(max_length = 300, default = "multiple")
    rating = models.DecimalField(max_digits = 4, decimal_places = 2, validators=[valid_rating], default=0.0)
    Ent = models.CharField(max_length = 200, choices = Contents_choices, default=Contents_choices[0][0])
    parent = models.CharField(max_length = 200)
    episode = models.IntegerField(default = 0, null=True, validators=[valid_episode])
    profile_pic = models.TextField(default = "image/400097700330_82090.jpg")
    status = models.CharField(max_length=255, choices=status_choices, default = status_choices[0][0])
    order = models.IntegerField(default = 0, null=True)
    genre = models.CharField(max_length=1000, default="")







