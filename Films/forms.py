from django import forms
from .models import Film
from django.forms import ValidationError
from django.conf import settings
import json
import os
def valid_json(value):
    try:
        json.load(value)
        return True
    except Exception:
        raise ValidationError('Upload json formatted file')

class FilmForm(forms.ModelForm):
    episode = forms.IntegerField(required=False)
    class Meta:
        model = Film
        fields = ['title', 'category', 'production', 'rating', 'Ent', 'episode', 'status']

class FilmForm_added(forms.Form):
    alternative_titles = forms.CharField(max_length=200)
    profile_pic = forms.ImageField()

class JsonForm(forms.Form):
    category = forms.ChoiceField(choices=Film.category_choices)
    file = forms.FileField(validators=[valid_json])

    def save(self, *args, **kwargs):
        values = self.clean()
        media_root = settings.MEDIA_ROOT
        path = os.path.join(media_root, 'import')
        path = os.path.join(path, values['category'])
        if os.path.exists(path):
            files = os.listdir(path)
            name = str(len(files))
        else:
            os.mkdir(path)
            name = '0'
        name += '.json'
        file_path = os.path.join(path, name)
        with open(file_path, 'wb+') as writer:
            for chunk in values['file'].chunks():
                writer.write(chunk)

class GetJsonForm(forms.Form):
    choose_file = forms.ChoiceField(choices=[])
    keys = forms.CharField(max_length=255, help_text="Dictionary key for the list of films")

class ConnectJsonForm(forms.Form):
    keys = forms.ChoiceField(choices=[])


class JsonStructForm(forms.Form):
    choose_key = forms.ChoiceField(choices=[])


