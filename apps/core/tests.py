from django.test import TestCase
from django.urls import reverse


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