from django.contrib import admin

from .models import Note


# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploader', 'downloads', 'created_at')
    list_filter = ('subject',)
