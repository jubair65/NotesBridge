from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from departments.models import Department, Subject
from notes.models import Note
from comments.models import Comment
from .forms import ProfileUpdateForm
from .models import Profile
from votes.models import Vote
from reports.models import Report
from django.db.models import Sum
from django.core.paginator import Paginator

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


@login_required
def browse_view(request):
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

    total_count = notes.count()

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notes': page_obj,
        'page_obj': page_obj,
        'subjects': subjects,
        'departments': departments,
        'total_count': total_count,
        'upvoted_note_ids': upvoted_note_ids,
        'downvoted_note_ids': downvoted_note_ids,
        'reported_note_ids': reported_note_ids,
    }

    return render(request, 'browse.html', context)

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    notes = Note.objects.filter(uploader=user).annotate(
        upvotes=Count('vote', filter=Q(vote__vote_type=1)),
        downvotes=Count('vote', filter=Q(vote__vote_type=0))
    ).order_by('-created_at')

    latest_note = notes.first()
    inferred_department = latest_note.subject.department.name if latest_note else "NotesBridge User"
    inferred_semester = latest_note.semester if latest_note else "Current Term"

    context = {
        'profile': profile,
        'notes': notes,
        'inferred_department': inferred_department,
        'inferred_semester': inferred_semester,
    }

    return render(request,'profiles/profile.html',context)

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profiles/edit_profile.html', {'form': form})


@login_required
def leaderboard_view(request):
    profiles = Profile.objects.select_related('user').order_by('-karma')


    all_profiles_list = list(profiles)
    top_contributor = all_profiles_list[0] if all_profiles_list else None
    top_karma = top_contributor.karma if top_contributor and top_contributor.karma > 0 else 1

    for i, p in enumerate(all_profiles_list, start=1):
        p.rank = i
        p.karma_percentage = min(100, int((p.karma / top_karma) * 100))

    top_3 = all_profiles_list[:3]

    total_karma = Profile.objects.aggregate(total=Sum('karma'))['total'] or 0
    total_uploads = Note.objects.count()
    active_scholars = Profile.objects.filter(karma__gt=0).count()

    paginator = Paginator(all_profiles_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'top_contributor': top_contributor,
        'top_3': top_3,
        'total_karma': total_karma,
        'total_uploads': total_uploads,
        'active_scholars': active_scholars,
    }

    return render(request, 'profiles/leaderboard.html', context)


