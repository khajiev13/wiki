from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.get_wiki, name="get_wiki"),
    path("search_results", views.search_results, name="search_results"),
    path("random_page", views.random_page, name="random_page"),
    path("add_page", views.add_page, name="add_page"),
    path("check_new_entry", views.check_new_entry, name="check_new_entry"),
    path("wiki/<str:name>/edit", views.edit_entry, name="edit_entry")
]
