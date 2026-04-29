from django.conf import settings
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    karma = models.FloatField(default=0)
    tier = models.CharField(max_length=20,default="Newcomer")

    total_uploads = models.PositiveIntegerField(default=0)
    total_upvotes = models.PositiveIntegerField(default=0)
    total_downvotes = models.PositiveIntegerField(default=0)
    total_downloads = models.PositiveIntegerField(default=0)
    moderation_penalty = models.FloatField(default=0)

    def __str__(self):
        return self.user.email
