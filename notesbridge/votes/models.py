from django.conf import settings
from django.db import models

from notes.models import Note


# Create your models here.
class Vote(models.Model):
    VOTE_TYPES = (
    (1,'Upvote'),
    (0,'Downvote'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=VOTE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'note'),)


    def __str__(self):
        return f"{self.user} → {self.note} ({self.vote_type})"
