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


@login_required
def upload_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploader = request.user


            files = request.FILES.getlist('file')


            if len(files) > 10:
                form.add_error(None, 'You can upload a maximum of 10 files per note.')
                return render(request, 'notes/upload.html',
                              {'form': form, 'error': 'You can upload a maximum of 10 files per note.'})

            if files:

                note.file = files[0]
                note.save()


                for f in files:
                    NoteFile.objects.create(note=note, file=f)
            else:
                note.save()

            return redirect('dashboard')
    else:
        form = NoteForm(user=request.user)

    return render(request, 'notes/upload.html', {'form': form})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if note.uploader != request.user:
        return redirect('dashboard')

    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note, user=request.user)
        if form.is_valid():
            note = form.save()


            files = request.FILES.getlist('file')
            current_count = note.additional_files.count()


            if current_count + len(files) > 10:
                remaining = 10 - current_count
                error = f'You can only add {remaining} more file(s). This note already has {current_count} attachment(s).'
                return render(request, 'notes/edit_note.html', {'form': form, 'note': note, 'error': error})

            for f in files:
                NoteFile.objects.create(note=note, file=f)

            return redirect('profile')
    else:
        form = NoteForm(instance=note, user=request.user)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)


    if note.uploader == request.user:
        profile = note.uploader.profile


        upvotes_count = note.vote_set.filter(vote_type=1).count()
        downvotes_count = note.vote_set.filter(vote_type=0).count()


        profile.total_uploads -= 1
        profile.total_upvotes -= upvotes_count
        profile.total_downvotes -= downvotes_count
        profile.total_downloads -= note.downloads


        profile.total_uploads = max(0, profile.total_uploads)
        profile.total_upvotes = max(0, profile.total_upvotes)
        profile.total_downvotes = max(0, profile.total_downvotes)
        profile.total_downloads = max(0, profile.total_downloads)


        update_karma(profile)

        note.delete()

    return redirect('profile')