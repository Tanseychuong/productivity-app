from django import forms

from apps.core.forms import BootstrapMixin

from .models import Contact


class ContactForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]