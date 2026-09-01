from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("zonas/", views.zonas_list, name="zonas_list"),
    path("zonas/<int:id>/", views.zona_detail, name="zona_detail"),
    path("dispositivos/", views.dispositivos_list, name="dispositivos_list"),
]