from django import forms

from apps.core.forms import BootstrapMixin

from .models import Task


class TaskForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "due_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }