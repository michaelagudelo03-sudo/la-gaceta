from django.urls import path
from . import views

app_name = "articulos"

urlpatterns = [
    path("", views.portada, name="portada"),
    path("buscar/", views.buscar, name="buscar"),
    path("categoria/<slug:slug>/", views.categoria, name="categoria"),
    path("a/<slug:slug>/", views.detalle, name="detalle"),
]
