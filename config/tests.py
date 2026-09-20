from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Contact, Journal, Note, Task


class PageLoadTests(TestCase):
    def test_all_pages_load(self):
        names = [
            "home", "contact_list", "contact_add",
            "journal_list", "journal_add",
            "note_list", "note_add",
            "task_list", "task_today", "task_add",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)


class ContactTests(TestCase):
    def test_add_edit_delete(self):
        r = self.client.post(reverse("contact_add"), {
            "first_name": "Ada", "last_name": "Lovelace",
            "phone": "0240000000", "email": "ada@example.com",
        })
        self.assertRedirects(r, reverse("contact_list"))
        contact = Contact.objects.get()

        self.client.post(reverse("contact_edit", args=[contact.pk]), {
            "first_name": "Augusta", "last_name": "Lovelace",
            "phone": "0240000000", "email": "ada@example.com",
        })
        contact.refresh_from_db()
        self.assertEqual(contact.first_name, "Augusta")

        self.client.post(reverse("contact_delete", args=[contact.pk]))
        self.assertEqual(Contact.objects.count(), 0)

    def test_delete_rejects_get(self):
        contact = Contact.objects.create(first_name="Ada")
        r = self.client.get(reverse("contact_delete", args=[contact.pk]))
        self.assertEqual(r.status_code, 405)
        self.assertEqual(Contact.objects.count(), 1)

    def test_search(self):
        Contact.objects.create(first_name="Ada", email="ada@example.com")
        Contact.objects.create(first_name="Grace")
        r = self.client.get(reverse("contact_list"), {"q": "ada"})
        self.assertContains(r, "Ada")
        self.assertNotContains(r, "Grace")


class JournalAndNoteTests(TestCase):
    def test_journal_create(self):
        self.client.post(reverse("journal_add"), {
            "title": "Day one", "content": "Started the Django move.",
            "entry_date": "2026-09-20",
        })
        self.assertEqual(Journal.objects.get().title, "Day one")

    def test_note_date_filter(self):
        Note.objects.create(title="Old note", content="x", date="2026-01-01")
        Note.objects.create(title="New note", content="y", date="2026-09-20")
        r = self.client.get(reverse("note_list"), {"date": "2026-09-20"})
        self.assertContains(r, "New note")
        self.assertNotContains(r, "Old note")

    def test_note_invalid_date_shows_error(self):
        r = self.client.get(reverse("note_list"), {"date": "not-a-date"})
        self.assertContains(r, "Invalid date")


class TaskTests(TestCase):
    def test_complete(self):
        task = Task.objects.create(name="Write tests")
        self.client.post(reverse("task_complete", args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_today_only_shows_due_today_and_incomplete(self):
        today = timezone.localdate()
        Task.objects.create(name="Due today", due_date=today)
        Task.objects.create(name="Due tomorrow", due_date=today + timedelta(days=1))
        Task.objects.create(name="Already done", due_date=today, completed=True)
        r = self.client.get(reverse("task_today"))
        self.assertContains(r, "Due today")
        self.assertNotContains(r, "Due tomorrow")
        self.assertNotContains(r, "Already done")