from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskList.as_view(), name="task_list"),
    path("today/", views.TaskToday.as_view(), name="task_today"),
    path("add/", views.TaskCreate.as_view(), name="task_add"),
    path("<int:pk>/edit/", views.TaskUpdate.as_view(), name="task_edit"),
    path("<int:pk>/complete/", views.task_complete, name="task_complete"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
]
