from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),

    path("contacts/", views.ContactList.as_view(), name="contact_list"),
    path("contacts/add/", views.ContactCreate.as_view(), name="contact_add"),
    path("contacts/<int:pk>/edit/", views.ContactUpdate.as_view(), name="contact_edit"),
    path("contacts/<int:pk>/delete/", views.contact_delete, name="contact_delete"),

    path("journals/", views.JournalList.as_view(), name="journal_list"),
    path("journals/add/", views.JournalCreate.as_view(), name="journal_add"),
    path("journals/<int:pk>/edit/", views.JournalUpdate.as_view(), name="journal_edit"),
    path("journals/<int:pk>/delete/", views.journal_delete, name="journal_delete"),

    path("notes/", views.NoteList.as_view(), name="note_list"),
    path("notes/add/", views.NoteCreate.as_view(), name="note_add"),
    path("notes/<int:pk>/edit/", views.NoteUpdate.as_view(), name="note_edit"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),

    path("tasks/", views.TaskList.as_view(), name="task_list"),
    path("tasks/today/", views.TaskToday.as_view(), name="task_today"),
    path("tasks/add/", views.TaskCreate.as_view(), name="task_add"),
    path("tasks/<int:pk>/edit/", views.TaskUpdate.as_view(), name="task_edit"),
    path("tasks/<int:pk>/complete/", views.task_complete, name="task_complete"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
]