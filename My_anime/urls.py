from django.urls import path
from . import views
urlpatterns = [
    path('', views.my_list_list, name = "my_list"),
    path('detail/<str:status>/<int:year>/<int:month>/<int:day>/', views.my_list_detail, name="my_list_detail"),
]
