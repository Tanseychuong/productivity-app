from django.urls import path

from . import views

urlpatterns = [
    path("", views.NoteList.as_view(), name="note_list"),
    path("add/", views.NoteCreate.as_view(), name="note_add"),
    path("<int:pk>/edit/", views.NoteUpdate.as_view(), name="note_edit"),
    path("<int:pk>/delete/", views.note_delete, name="note_delete"),
]