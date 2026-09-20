from django.contrib import admin

from .models import Contact, Journal, Note, Task

admin.site.register([Contact, Journal, Note, Task])