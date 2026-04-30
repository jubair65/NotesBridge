from django.conf import settings
from django.db import models

from departments.models import Subject, Department


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    file = models.FileField(upload_to='notes/', blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professor = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)

    downloads = models.PositiveIntegerField(default=0)

    # Moderation fields
    is_flagged = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    report_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='additional_files')
    file = models.FileField(upload_to='notes/')

    def __str__(self):
        return f"{self.note.title} - {self.file.name}"
