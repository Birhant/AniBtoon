from os import name
from django.urls import path
from .views import add_local, local_list
from .views import video_list

urlpatterns = [
    path('add/', add_local, name = "ADD_DIRS"),
    path('list/', local_list, name = "Local_files"),
    path('list/<str:category>/', local_list, name = "Local_files"),
    path('list/<str:category>/<int:index>/', local_list, name = "Local_files_index"),
    path('list/<str:category>/<int:index>/<str:folder>/', video_list, name = "Local_video"),
]

