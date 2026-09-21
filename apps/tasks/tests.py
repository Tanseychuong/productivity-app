from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


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