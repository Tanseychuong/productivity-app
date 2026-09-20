import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date

from planner.models import Contact, Journal, Note, Task


def pick(item, *keys, default=""):
    """Return the first non-empty value among several possible key names."""
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return default


def to_date(value):
    if not value or not isinstance(value, str):
        return None
    return parse_date(value.strip()[:10])  # handles "2025-09-15" and ISO datetimes


def to_bool(value):
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "done", "completed", "complete"}
    return bool(value)


class Command(BaseCommand):
    help = "Import contacts/journals/notes/tasks from the old JSON files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            default=str(Path(settings.BASE_DIR) / "Backend" / "data"),
        )
        parser.add_argument("--dry-run", action="store_true")

    def load(self, data_dir, name):
        path = Path(data_dir) / f"{name}.json"
        if not path.exists():
            self.stdout.write(self.style.WARNING(f"{path} not found, skipping"))
            return []
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise CommandError(f"{path} is not a JSON list; adjust the importer.")
        return data

    @transaction.atomic
    def handle(self, *args, **opts):
        d = opts["data_dir"]
        today = timezone.localdate()
        bad_dates = 0

        for c in self.load(d, "contacts"):
            Contact.objects.create(
                first_name=pick(c, "first_name", "first", "First Name"),
                last_name=pick(c, "last_name", "last", "Last Name"),
                phone=pick(c, "phone", "Phone"),
                email=pick(c, "email", "Email"),
            )

        for j in self.load(d, "journals"):
            entry_date = to_date(pick(j, "date", "created", "timestamp", default=None))
            bad_dates += entry_date is None
            Journal.objects.create(
                title=pick(j, "title", "Title", default="Untitled"),
                content=pick(j, "content", "entry", "body", "text"),
                entry_date=entry_date or today,
            )

        for n in self.load(d, "notes"):
            note_date = to_date(pick(n, "date", "created", "timestamp", default=None))
            bad_dates += note_date is None
            Note.objects.create(
                title=pick(n, "title", "Title", default="Untitled"),
                content=pick(n, "content", "note", "body", "text"),
                date=note_date or today,
            )

        for t in self.load(d, "tasks"):
            Task.objects.create(
                name=pick(t, "name", "title", "task", default="Untitled"),
                description=pick(t, "description", "details"),
                due_date=to_date(pick(t, "due_date", "due", default=None)),
                completed=to_bool(pick(t, "completed", "done", "status", default=False)),
            )

        counts = {m.__name__: m.objects.count() for m in (Contact, Journal, Note, Task)}
        self.stdout.write(self.style.SUCCESS(f"Imported: {counts}"))
        if bad_dates:
            self.stdout.write(
                self.style.WARNING(f"{bad_dates} journal/note dates unparseable; used today.")
            )

        if opts["dry_run"]:
            transaction.set_rollback(True)
            self.stdout.write("Dry run: rolled back, nothing saved.")