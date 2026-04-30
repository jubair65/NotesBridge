from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vote
from notes.models import Note
from profiles.utils import update_karma
from django.http import JsonResponse

@login_required
def vote_note(request, note_id, value):
    note = get_object_or_404(Note, id=note_id)
    user = request.user

    vote = Vote.objects.filter(user=user, note=note).first()
    profile = note.uploader.profile


    def handle_response():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'upvotes': Vote.objects.filter(note=note, vote_type=1).count(),
                'downvotes': Vote.objects.filter(note=note, vote_type=0).count(),
            })
        return redirect('dashboard')


    if vote:

        if vote.vote_type == value:
            if value == 1:
                profile.total_upvotes -= 1
            else:
                profile.total_downvotes -= 1

            vote.delete()
            update_karma(profile)
            return handle_response()


        if vote.vote_type == 1:
            profile.total_upvotes -= 1
        else:
            profile.total_downvotes -= 1

        vote.vote_type = value
        vote.save()

        if value == 1:
            profile.total_upvotes += 1
        else:
            profile.total_downvotes += 1

        update_karma(profile)
        return handle_response()


    Vote.objects.create(user=user, note=note, vote_type=value)

    if value == 1:
        profile.total_upvotes += 1
    else:
        profile.total_downvotes += 1

    update_karma(profile)

    return handle_response()