from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import ContactForm, JournalForm, NoteForm, TaskForm
from .models import Contact, Journal, Note, Task


class Home(TemplateView):
    template_name = "planner/home.html"


class FormPageMixin(SuccessMessageMixin):
    """One shared form.html for every add/edit page."""

    template_name = "planner/form.html"
    page_title = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.page_title
        ctx["cancel_url"] = self.success_url
        return ctx


def make_delete_view(model, list_url, label):
    @require_POST
    def view(request, pk):
        get_object_or_404(model, pk=pk).delete()
        messages.success(request, f"{label} deleted.")
        return redirect(list_url)

    return view


# ---------- Contacts ----------
class ContactList(ListView):
    model = Contact
    template_name = "planner/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(phone__icontains=q)
                | Q(email__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class ContactCreate(FormPageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    page_title = "Add contact"
    success_url = reverse_lazy("contact_list")
    success_message = "Contact added."


class ContactUpdate(FormPageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    page_title = "Edit contact"
    success_url = reverse_lazy("contact_list")
    success_message = "Contact updated."


contact_delete = make_delete_view(Contact, "contact_list", "Contact")


# ---------- Journals ----------
class JournalList(ListView):
    model = Journal
    template_name = "planner/journal_list.html"
    context_object_name = "journals"


class JournalCreate(FormPageMixin, CreateView):
    model = Journal
    form_class = JournalForm
    page_title = "New journal entry"
    success_url = reverse_lazy("journal_list")
    success_message = "Journal entry added."


class JournalUpdate(FormPageMixin, UpdateView):
    model = Journal
    form_class = JournalForm
    page_title = "Edit journal entry"
    success_url = reverse_lazy("journal_list")
    success_message = "Journal entry updated."


journal_delete = make_delete_view(Journal, "journal_list", "Journal entry")


# ---------- Notes ----------
class NoteList(ListView):
    model = Note
    template_name = "planner/note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        qs = super().get_queryset()
        raw = self.request.GET.get("date", "").strip()
        if raw:
            parsed = parse_date(raw)
            if parsed is None:
                messages.error(self.request, "Invalid date. Use YYYY-MM-DD.")
            else:
                qs = qs.filter(date=parsed)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["date_filter"] = self.request.GET.get("date", "").strip()
        return ctx


class NoteCreate(FormPageMixin, CreateView):
    model = Note
    form_class = NoteForm
    page_title = "Add note"
    success_url = reverse_lazy("note_list")
    success_message = "Note added."


class NoteUpdate(FormPageMixin, UpdateView):
    model = Note
    form_class = NoteForm
    page_title = "Edit note"
    success_url = reverse_lazy("note_list")
    success_message = "Note updated."


note_delete = make_delete_view(Note, "note_list", "Note")


# ---------- Tasks ----------
class TaskList(ListView):
    model = Task
    template_name = "planner/task_list.html"
    context_object_name = "tasks"


class TaskToday(ListView):
    model = Task
    template_name = "planner/task_today.html"
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