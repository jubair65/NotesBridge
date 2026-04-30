from django.urls import path

from .views import report_note

urlpatterns = [
    path('note/<int:note_id>/',report_note,name='report_note'),
]