from django.contrib import admin
from reports.models import Report


# Register your models here.
@admin.register(Report)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user','note','reason','created_at')
    list_filter = ('reason',)
    search_fields = ('details',)
