from django import forms
from django.core.exceptions import ValidationError
import os
from django.conf import settings

media_root = settings.MEDIA_ROOT

def add_dirs(username, category, dir):
    dir_path = os.path.join(media_root, username)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    dir_path = os.path.join(dir_path, 'local_dir.txt')
    sep = "| |"
    text = category+sep+dir
    with open(dir_path, 'w+')as writer:
        writer.write(text)
        writer.write('\n')

def get_dirs(username, category = None):
    dir_path = os.path.join(media_root, username)
    dir_path = os.path.join(dir_path, 'local_dir.txt')
    if os.path.exists(dir_path):
        sep = "| |"
        with open(dir_path, 'r')as reader:
            files = []
            all = reader.read().split('\n')
        all.pop()
        for row in all:
            categories = row.split(sep=sep)
            if categories[0] == category or category is None:
                files.append(categories[1])
    else:
        files = []
    return files

def valid_directory(value):
    if os.path.exists(value):
        if os.path.isdir(value):
            return True
    else:
        raise ValidationError( ( 'The directory doesnot exist' ), code=' invalid' )

def unique_directory(value):
    files = get_dirs()
    if value in files:
        raise ValidationError( ( 'The directory is already added' ), code=' invalid' )
    else:
        return True

def valid_storage(value):
    if os.path.exists(value):
        if os.path.isdir(value):
            return True
    else:
        raise ValidationError( ( 'The directory doesnot exist' ), code=' invalid' )

class Anime_Dirs(forms.Form):
    categories = (
        ('anime',"Anime"),
        ('cartoon',"Cartoon"),
        ('manga',"Manga"),
        ('comic',"Comic")
    )
    dir = forms.CharField(max_length=500, validators=[valid_directory])
    category = forms.ChoiceField(choices=categories, initial=categories[0][0])





