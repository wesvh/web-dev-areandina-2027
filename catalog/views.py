from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import VoteForm
from .models import Category, Edition, Poll, Vote
from .voting import VoteRejected, cast_vote, validate_vote

PUBLIC_POLL_STATUSES = (Poll.Status.OPEN, Poll.Status.CLOSED)


def user_vote_in_category(user, category_id):
    if not user.is_authenticated:
        return None
    return (
        Vote.objects.select_related("option", "poll")
        .filter(user=user, category_id=category_id)
        .first()
    )


def home(request):
    editions = Edition.objects.prefetch_related("categories").all()
    return render(request, "catalog/home.html", {"editions": editions})


def edition_detail(request, pk):
    edition = get_object_or_404(Edition, pk=pk)
    categories = edition.categories.prefetch_related("polls").all()
    return render(
        request,
        "catalog/edition_detail.html",
        {"edition": edition, "categories": categories},
    )


def category_detail(request, pk):
    category = get_object_or_404(Category.objects.select_related("edition"), pk=pk)
    polls = category.polls.filter(status__in=PUBLIC_POLL_STATUSES)
    return render(
        request,
        "catalog/category_detail.html",
        {
            "category": category,
            "polls": polls,
            "existing_vote": user_vote_in_category(request.user, category.pk),
        },
    )


def poll_detail(request, pk):
    poll = get_object_or_404(
        Poll.objects.select_related("category", "category__edition").prefetch_related("options"),
        pk=pk,
        status__in=PUBLIC_POLL_STATUSES,
    )
    existing_vote = user_vote_in_category(request.user, poll.category_id)
    can_vote = (
        request.user.is_authenticated
        and poll.status == Poll.Status.OPEN
        and existing_vote is None
    )
    return render(
        request,
        "catalog/poll_detail.html",
        {
            "poll": poll,
            "options": poll.options.all(),
            "existing_vote": existing_vote,
            "form": VoteForm(poll) if can_vote else None,
        },
    )


@login_required
@require_POST
def vote(request, pk):
    """Select → confirm → validate in Django → store in MySQL."""
    poll = get_object_or_404(
        Poll.objects.select_related("category__edition"), pk=pk, status__in=PUBLIC_POLL_STATUSES
    )
    form = VoteForm(poll, request.POST)
    try:
        if not form.is_valid():
            missing = form.has_error("option", "required")
            raise VoteRejected("option_required" if missing else "option_mismatch")
        option = form.cleaned_data["option"]
        if request.POST.get("confirm") != "1":
            validate_vote(request.user, poll, option.pk)
            return render(request, "catalog/vote_confirm.html", {"poll": poll, "option": option})
        cast_vote(request.user, poll, option.pk)
    except VoteRejected as rejection:
        messages.error(request, str(rejection))
        return redirect("catalog:poll", pk=poll.pk)
    messages.success(request, f"Voto registrado: {option.name} en {poll.category.name}.")
    return redirect("catalog:my-votes")


@login_required
def my_votes(request):
    votes = request.user.votes.select_related("edition", "category", "poll", "option")
    return render(request, "catalog/my_votes.html", {"votes": votes})


def health(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})
