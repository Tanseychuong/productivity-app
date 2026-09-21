from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContactList.as_view(), name="contact_list"),
    path("add/", views.ContactCreate.as_view(), name="contact_add"),
    path("<int:pk>/edit/", views.ContactUpdate.as_view(), name="contact_edit"),
    path("<int:pk>/delete/", views.contact_delete, name="contact_delete"),
]