"""Input adapter (web). Catalog pages read the ORM directly; votes and results go through the core."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .core.domain import VoteRejected
from .core.services import VotingService
from .forms import VoteForm
from .models import Category, Edition, Poll, Vote
from .repository import DjangoVoteRepository

# Composition root: the only line where the core is connected to its MySQL adapter.
voting = VotingService(DjangoVoteRepository())


# --- Read-only catalog pages (classic Django MVT) ---


def home(request):
    editions = Edition.objects.all()
    return render(request, "catalog/home.html", {"editions": editions})


def edition_detail(request, pk):
    edition = get_object_or_404(Edition, pk=pk)
    categories = edition.categories.all()
    return render(
        request, "catalog/edition_detail.html", {"edition": edition, "categories": categories}
    )


def category_detail(request, pk):
    category = get_object_or_404(Category.objects.select_related("edition"), pk=pk)
    context = {
        "category": category,
        "polls": category.polls.filter(status__in=Poll.PUBLIC_STATUSES),
        "existing_vote": vote_in_category(request.user, category.pk),
    }
    return render(request, "catalog/category_detail.html", context)


def poll_detail(request, pk):
    poll = get_object_or_404(
        Poll.objects.select_related("category__edition").prefetch_related("options"),
        pk=pk,
        status__in=Poll.PUBLIC_STATUSES,
    )
    existing_vote = vote_in_category(request.user, poll.category_id)
    can_vote = (
        request.user.is_authenticated and poll.status == Poll.Status.OPEN and not existing_vote
    )
    context = {
        "poll": poll,
        "options": poll.options.all(),
        "existing_vote": existing_vote,
        "form": VoteForm(poll) if can_vote else None,
    }
    return render(request, "catalog/poll_detail.html", context)


@login_required
def my_votes(request):
    votes = request.user.votes.select_related("edition", "category", "poll", "option")
    return render(request, "catalog/my_votes.html", {"votes": votes})


def vote_in_category(user, category_id):
    """The vote the user already cast in this category, or None."""
    if not user.is_authenticated:
        return None
    return Vote.objects.select_related("option", "poll").filter(
        user=user, category_id=category_id
    ).first()


# --- Voting and results (through the hexagon core) ---


@login_required
@require_POST
def vote(request, pk):
    """Step 1 shows the confirmation page; step 2 (confirm=1) stores the vote."""
    poll = get_object_or_404(
        Poll.objects.select_related("category__edition"), pk=pk, status__in=Poll.PUBLIC_STATUSES
    )
    try:
        option = selected_option(VoteForm(poll, request.POST))
        if request.POST.get("confirm") != "1":
            voting.check(request.user.pk, poll.pk, option.pk)
            return render(request, "catalog/vote_confirm.html", {"poll": poll, "option": option})
        voting.cast(request.user.pk, poll.pk, option.pk)
    except VoteRejected as rejection:
        messages.error(request, str(rejection))
        return redirect("catalog:poll", pk=poll.pk)
    messages.success(request, f"Voto registrado: {option.name} en {poll.category.name}.")
    return redirect("catalog:my-votes")


def selected_option(form):
    """The option chosen in the form, or the rule the submission broke."""
    if form.is_valid():
        return form.cleaned_data["option"]
    if form.has_error("option", "required"):
        raise VoteRejected("option_required")
    raise VoteRejected("option_mismatch")


def results(request):
    return render(request, "catalog/results.html", {"results": voting.results()})
