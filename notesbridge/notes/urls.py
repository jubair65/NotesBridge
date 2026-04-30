from django.urls import path
from .views import download_note,upload_note,edit_note,delete_note,note_detail_view,download_zip
urlpatterns = [
    path('download/<int:note_id>/', download_note, name='download_note'),
    path('upload/', upload_note, name='upload'),
    path('edit/<int:note_id>/', edit_note, name='edit_note'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),
    path('note/<int:note_id>/', note_detail_view, name='note_detail'),
    path('download-zip/<int:note_id>/', download_zip, name='download_zip'),
]