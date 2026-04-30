from django.urls import path
from .views import download_note,upload_note,edit_note,delete_note
urlpatterns = [
    path('download/<int:note_id>/', download_note, name='download_note'),
    path('upload/', upload_note, name='upload'),
    path('edit/<int:note_id>/', edit_note, name='edit_note'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),

]