from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.views import FormPageMixin, make_delete_view

from .forms import NoteForm
from .models import Note


class NoteList(ListView):
    model = Note
    template_name = "notes/list.html"
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