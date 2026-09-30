from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('home', views.Home, name="homepage"),
    path('create', views.Create, name="create"),
    path('edit/<int:empid>', views.Edit, name="edit"),
    path('delete/<int:empid>', views.Delete, name="delete"),
]