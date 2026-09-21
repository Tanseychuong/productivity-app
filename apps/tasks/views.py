from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.views import FormPageMixin, make_delete_view

from .forms import TaskForm
from .models import Task


class TaskList(ListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"


class TaskToday(ListView):
    model = Task
    template_name = "tasks/today.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(due_date=timezone.localdate(), completed=False)


class TaskCreate(FormPageMixin, CreateView):
    model = Task
    form_class = TaskForm
    page_title = "Add task"
    success_url = reverse_lazy("task_list")
    success_message = "Task added."


class TaskUpdate(FormPageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    page_title = "Edit task"
    success_url = reverse_lazy("task_list")
    success_message = "Task updated."


@require_POST
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save(update_fields=["completed"])
    messages.success(request, "Task marked as completed.")
    return redirect("task_list")


task_delete = make_delete_view(Task, "task_list", "Task")