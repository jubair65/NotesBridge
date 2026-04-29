
# Register your models here.
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'karma',
        'tier',
        'total_uploads',
        'total_upvotes',
        'total_downvotes',
        'total_downloads'
    )
    search_fields = ('user__email',)

