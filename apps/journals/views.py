from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.views import FormPageMixin, make_delete_view

from .forms import JournalForm
from .models import Journal


class JournalList(ListView):
    model = Journal
    template_name = "journals/list.html"
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