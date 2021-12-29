from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display , name="display"),
    path("New_entry", views.New_entry , name="New_entry"),
    path("/", views.search , name="search"),
    path("Random", views.Random , name="Random"),
    path("Edit/<str:title>", views.Edit , name="Edit"),
]
