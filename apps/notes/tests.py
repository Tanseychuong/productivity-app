from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteTests(TestCase):
    def test_note_date_filter(self):
        Note.objects.create(title="Old note", content="x", date="2026-01-01")
        Note.objects.create(title="New note", content="y", date="2026-09-20")
        r = self.client.get(reverse("note_list"), {"date": "2026-09-20"})
        self.assertContains(r, "New note")
        self.assertNotContains(r, "Old note")

    def test_note_invalid_date_shows_error(self):
        r = self.client.get(reverse("note_list"), {"date": "not-a-date"})
        self.assertContains(r, "Invalid date")