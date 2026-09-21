from django.urls import path

from . import views

urlpatterns = [
    path("", views.JournalList.as_view(), name="journal_list"),
    path("add/", views.JournalCreate.as_view(), name="journal_add"),
    path("<int:pk>/edit/", views.JournalUpdate.as_view(), name="journal_edit"),
    path("<int:pk>/delete/", views.journal_delete, name="journal_delete"),
]