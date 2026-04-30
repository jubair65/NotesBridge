from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Note
from profiles.utils import update_karma


@receiver(post_save,sender=Note)
def update_profile_on_upload(sender,instance,created,**kwargs):
    if created:
        profile = instance.uploader.profile

        profile.total_uploads += 1
        update_karma(profile)
