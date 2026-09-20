from django import forms

from .models import Contact, Journal, Note, Task


class BootstrapMixin:
    """Adds Bootstrap classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class ContactForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]


class JournalForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content", "entry_date"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8}),
            "entry_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class NoteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "date"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class TaskForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "due_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }