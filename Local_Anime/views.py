from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
import os
from .forms import Anime_Dirs, add_dirs, get_dirs
from .animes import Anime_files
from Home.views import signed_in
# Create your views here.


@signed_in
def add_local(request):
    if request.method == "POST":
        form = Anime_Dirs(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = request.user.username
            add_dirs(username, data['category'], data['dir'])
            return redirect('Local_files', data['category'])
    else:
        form = Anime_Dirs
    Contents = {'title':"Add directory",'form': form}
    return render(request, "local/add_dirs.html", Contents)


@signed_in
def local_list(request, category="anime", index=1):
    index-=1
    username = request.user.username
    files = get_dirs(username, category)
    if len(files)<1:
        messages.warning(request, "Add at least 1 directory")
        return redirect("ADD_DIRS")
    animes = Anime_files(files[index])
    anime_list = animes.anime_list
    picture = os.path.join(settings.MEDIA_URL, "image/400097700330_82090.jpg")
    Contents = {'title':"Local directories", 'anime_list':anime_list, 'category':category, 'picture':picture, 'files':files, 'index':index}
    return render(request, "local/local_list.html", Contents)

@signed_in
def video_list(request, category, index, folder):
    username = request.user.username
    files = get_dirs(username, category)
    animes = Anime_files(files[index])
    print(animes.anime.keys())
    elements = animes.anime[folder]
    context = {'title': folder, 'elements':elements}
    return render(request, 'local/video.html', context)





