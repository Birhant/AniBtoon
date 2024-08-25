from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os
from .models import My_List
# Create your views here.

def my_list_detail(request, status, year, month, day):
    my_list_obj = get_object_or_404(My_List, status = status, registered__year = year, registered__month=month, registered__day = day)
    Contents = {'my_list':my_list_obj}
    return render(request, "my/my_list_detail.html", Contents)

def my_list_list(request, status = None):
    if status is None:
        objects = My_List.objects.all()
    picture = os.path.join(settings.MEDIA_URL, "image/400097700330_82090.jpg")
    context = {'title': 'My list', 'picture': picture}
    return render(request, 'my/my_list.html', context)




