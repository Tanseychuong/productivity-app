from django.db import models
from django.utils import timezone


class Journal(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    entry_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-entry_date", "-id"]

    def __str__(self):
        return self.title