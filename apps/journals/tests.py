from django.test import TestCase
from django.urls import reverse

from .models import Journal


class JournalTests(TestCase):
    def test_journal_create(self):
        self.client.post(reverse("journal_add"), {
            "title": "Day one", "content": "Started the Django move.",
            "entry_date": "2026-09-20",
        })
        self.assertEqual(Journal.objects.get().title, "Day one")