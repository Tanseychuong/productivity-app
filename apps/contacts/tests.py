from django.test import TestCase
from django.urls import reverse

from .models import Contact


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