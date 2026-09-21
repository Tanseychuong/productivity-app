from django.db import models


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