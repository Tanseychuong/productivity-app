from django import forms

from apps.core.forms import BootstrapMixin

from .models import Journal


class JournalForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["title", "content", "entry_date"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8}),
            "entry_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }