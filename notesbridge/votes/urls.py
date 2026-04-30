from os import name
from django.urls import path
from .views import vote_note

urlpatterns = [
    path('vote/<int:note_id>/<int:value>/',vote_note,name='vote_note'),
]