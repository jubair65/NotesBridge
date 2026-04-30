from django.urls import path
from .views import download_note
urlpatterns = [
    path('download/<int:note_id>/', download_note, name='download_note'),
]