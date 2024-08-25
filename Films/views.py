from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import ListView
import json
from .models import Film
from .forms import JsonForm, ConnectJsonForm, GetJsonForm
from .forms import FilmForm, FilmForm_added, JsonStructForm
from django.conf import settings
import os
from Home.views import signed_in

# Create your views here.

def get_film(parent = False, category=None):
    film_titles = [None]
    film_objs = Film.objects.filter()
    for film in film_objs:
        if category is None or category == film.category:
            if film.Ent=='original':
                film_titles.append(film.title)
            elif not parent:
                film_titles.append(film.parent+' '+film.title)
    return film_titles

@signed_in
def add_film(request):
    film_titles = get_film(parent = True)
    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            values = form.clean()
            form.save()
            obj = Film.objects.get(title = values['title'])
            obj.parent = request.POST['parent']
            obj.save()
    else:
        form = FilmForm()
    context = {'title': "Add film", 'form':form, 'film_titles':film_titles}
    return render(request, 'film/add_film.html', context)

@signed_in
def update_film(request):
    film_titles = get_film()
    film_titles.pop(0)
    if request.method == "POST":
        form = FilmForm_added(request.POST)
    form = FilmForm_added()
        
    Ent = {'title': "Add film", 'form':form, 'film_titles':film_titles}
    return render(request, 'film/update_film.html', Ent)

@signed_in
def import_json(request):
    if request.method == "POST":
        form = JsonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('json to film', form.data['category'])
    form = JsonForm()
    Ent = {'title': 'import from json', 'form':form}
    return render(request, 'json/upload_json.html', Ent)

def read(category, file):
    media_root = settings.MEDIA_ROOT
    path = os.path.join(media_root, 'import')
    path = os.path.join(path, category)
    file_path = os.path.join(path, file)
    with open(file_path, 'rb') as reader:
        file_obj = json.load(reader)
    return file_obj

@signed_in
def json_film(request, category):
    media_root = settings.MEDIA_ROOT
    path = os.path.join(media_root, 'import')
    path = os.path.join(path, category)
    if not os.path.exists(path):
        return redirect("Add Film")
    if request.method == "POST":
        form = GetJsonForm(request.POST)
        file = form.data.get('choose_file')
        key = form.data.get('keys')
        file_obj = read(category, file)
        if key in list(file_obj.keys()):
            return redirect('connect json', category, file, key)
    form = GetJsonForm()
    dirs = os.listdir(path)
    dir_choices = []
    for dir in dirs:
        dir_choices.append((dir, dir))
    dir_choices = tuple(dir_choices)
    form.fields['choose_file'].choices = dir_choices
    Ent = {'title': 'json to film', 'form':form}
    return render(request, 'json/json_to_film.html', Ent)

def save_film(title, alternative_title, Ent, episode, status, genre):
    instant = Film(
        title=title,
        alternative_title = alternative_title,
        Ent = Ent,
        episode = episode,
        status = status,
        genre = genre
    )
    try:
        instant.save()
    except Exception:
        print(title+' already exists')

def choices(obj, value, choice_map, model_choice):
    if obj[value] not in list(choice_map.keys()):
        index = len(list(choice_map.keys()))
        choice_map[obj[value]] = model_choice[index][0]
    new = choice_map[obj[value]]
    return new

def to_str(obj):
    if type(obj)==list:
        new = ('| |').join(obj)
    return new


def save_films(json_obj, title, alternative_title, Ent, episode, status, genre):
    Contents_map = {}
    status_map = {}
    for obj in json_obj:
        Contents_ = choices(obj, Ent, Contents_map, Film.Contents_choices)
        status_ = choices(obj, status, status_map, Film.status_choices)
        alternative_title_ = to_str(obj[alternative_title])
        genre_ = to_str(obj[genre])
        save_film(obj[title], alternative_title_, Contents_, int(obj[episode]), status_, genre_)
    return Contents_map, status_map

@signed_in
def connect_json(request, category, file, key):
    file_obj = read(category, file)
    json_obj = file_obj[key]
    keys = list(json_obj[0].keys())
    fields = ["title", "alternative_title", "Ent", "episode", "status", "genre" ]
    Ent = {'title': 'connect json','fields':fields, 'keys':keys}
    if request.method == "POST":
        Contents_map, status_map = save_films(
        json_obj,
        request.POST['title'],
        request.POST['alternative_title'],
        request.POST['Ent'],
        request.POST['episode'],
        request.POST['status'],
        request.POST['genre']
        )
        print(Contents_map)
        print(status_map)
    return render(request, 'json/connect_json.html', Ent)

class list_film(ListView):
    context_object_name = "films"
    paginate_by = 2
    template_name = 'film/list_film.html'
    def get_queryset(self):
        objects = get_list_or_404(Film, category = self.kwargs['category'])
        return Film.objects.filter(category = self.kwargs['category'], Ent = 'original').order_by('title')


