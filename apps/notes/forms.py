from django import forms

from apps.core.forms import BootstrapMixin

from .models import Note


class NoteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "date"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }