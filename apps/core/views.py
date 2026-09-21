from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "core/home.html"


class FormPageMixin(SuccessMessageMixin):
    """One shared form.html for every add/edit page."""

    template_name = "form.html"
    page_title = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.page_title
        ctx["cancel_url"] = self.success_url
        return ctx


def make_delete_view(model, list_url, label):
    """POST-only delete view for a model."""

    @require_POST
    def view(request, pk):
        get_object_or_404(model, pk=pk).delete()
        messages.success(request, f"{label} deleted.")
        return redirect(list_url)

    return view