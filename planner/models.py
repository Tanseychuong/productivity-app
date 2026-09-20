from django.db import models
from django.utils import timezone


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Journal(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    entry_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-entry_date", "-id"]

    def __str__(self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return self.title


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        # incomplete first, then soonest due date (undated last)
        ordering = ["completed", models.F("due_date").asc(nulls_last=True), "id"]

    def __str__(self):
        return self.name