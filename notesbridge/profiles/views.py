from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render
from departments.models import Department, Subject
from notes.models import Note
from comments.models import Comment
from votes.models import Vote
from reports.models import Report

@login_required
def dashboard_view(request):
    profile = request.user.profile
    notes = Note.objects.filter(is_hidden=False, is_deleted=False).annotate(
        upvotes=Count('vote', filter=Q(vote__vote_type=1)),
        downvotes=Count('vote', filter=Q(vote__vote_type=0)),
        comment_count=Count('comments')
    ).order_by('-created_at')


    query = request.GET.get('q')
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )


    subject_id = request.GET.get('subject')
    if subject_id and subject_id != "":
        notes = notes.filter(subject_id=subject_id)


    department_id = request.GET.get('department')
    if department_id and department_id != "":
        notes = notes.filter(subject__department_id=department_id)

    subjects = Subject.objects.all()
    departments = Department.objects.all()


    user_votes = Vote.objects.filter(user=request.user)
    upvoted_note_ids = list(user_votes.filter(vote_type=1).values_list('note_id', flat=True))
    downvoted_note_ids = list(user_votes.filter(vote_type=0).values_list('note_id', flat=True))


    reported_note_ids = list(Report.objects.filter(user=request.user).values_list('note_id', flat=True))


    notes = notes[:3]

    context = {
        'profile': profile,
        'notes': notes,
        'subjects': subjects,
        'departments': departments,
        'upvoted_note_ids': upvoted_note_ids,
        'downvoted_note_ids': downvoted_note_ids,
        'reported_note_ids': reported_note_ids,
    }

    return render(request, 'dashboard.html', context)


