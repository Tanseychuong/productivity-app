from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.views import FormPageMixin, make_delete_view

from .forms import ContactForm
from .models import Contact


class ContactList(ListView):
    model = Contact
    template_name = "contacts/list.html"
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