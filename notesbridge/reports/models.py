from django.conf import settings
from django.db import models

from notes.models import Note


# Create your models here.
class Report(models.Model):

    REPORT_CHOICES = [
        ('spam', 'Spam'),
        ('copyright', 'Copyright Violation'),
        ('wrong', 'Incorrect Content'),
        ('offensive', 'Offensive Content'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    reason = models.CharField(max_length=50, choices=REPORT_CHOICES)
    details = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')

    def __str__(self):
        return f"{self.user} reported {self.note}"