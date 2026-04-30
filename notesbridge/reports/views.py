from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from notes.forms import NoteForm
from notes.models import Note
from .forms import ReportForm
from .models import Report


# Create your views here.

@login_required
def report_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        if Report.objects.filter(user=request.user, note=note).exists():

            return redirect('note_detail', note_id=note.id)

        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.note = note
            report.save()


            note.report_count += 1
            if note.report_count >= 10:
                if not note.is_deleted:
                    note.is_deleted = True
                    note.is_hidden = True


                    uploader_profile = note.uploader.profile


                    from votes.models import Vote
                    upvotes_count = Vote.objects.filter(note=note, vote_type=1).count()
                    downvotes_count = Vote.objects.filter(note=note, vote_type=0).count()

                    uploader_profile.total_uploads = max(0, uploader_profile.total_uploads - 1)
                    uploader_profile.total_upvotes = max(0, uploader_profile.total_upvotes - upvotes_count)
                    uploader_profile.total_downvotes = max(0, uploader_profile.total_downvotes - downvotes_count)
                    uploader_profile.total_downloads = max(0, uploader_profile.total_downloads - note.downloads)


                    uploader_profile.moderation_penalty += 5

                    from profiles.utils import update_karma
                    update_karma(uploader_profile)
            elif note.report_count >= 5:
                note.is_hidden = True
            elif note.report_count >= 3:
                note.is_flagged = True

            note.save()
            return redirect('note_detail', note_id=note.id)
    else:
        form = ReportForm()

    context = {'form': form, 'note': note}
    return render(request, 'reports/report.html', context)

