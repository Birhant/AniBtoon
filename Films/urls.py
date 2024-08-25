from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_film, name='Add film'),
    path('import/', views.import_json, name='upload json'),
    path('convert/<str:category>', views.json_film, name='json to film'),
    path('connect/<str:category>/<str:file>/<str:key>', views.connect_json, name='connect json'),
    path('update/', views.update_film, name='Update film'),
    path('list/<category>/', views.list_film.as_view(), name='Films'),
]



