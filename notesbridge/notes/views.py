from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from notes.forms import NoteForm
from notes.models import Note, NoteFile
from comments.forms import CommentForm
from profiles.utils import update_karma
from notes.models import Note
import os
import zipfile
import io
from django.http import FileResponse, HttpResponse
from votes.models import Vote
from reports.models import Report


@login_required
def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    note.downloads += 1
    note.save()

    profile = note.uploader.profile
    profile.total_downloads += 1
    profile.save()

    if note.file:
        return FileResponse(open(note.file.path, 'rb'), as_attachment=True, filename=os.path.basename(note.file.name))

    return redirect('dashboard')