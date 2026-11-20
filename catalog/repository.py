"""Output adapter: implements the VoteRepository port with the Django ORM over MySQL."""
from django.db import IntegrityError, transaction
from django.db.models import Count, Prefetch

from .core.domain import VoteFacts, VoteRejected, build_poll_result
from .models import Option, Poll, Vote


class DjangoVoteRepository:
    def get_vote_facts(self, voter_id, poll_id, option_id):
        poll = Poll.objects.get(pk=poll_id)
        return VoteFacts(
            poll_is_open=poll.status == Poll.Status.OPEN,
            option_belongs_to_poll=poll.options.filter(pk=option_id).exists(),
            already_voted_in_category=Vote.objects.filter(
                user_id=voter_id, category_id=poll.category_id
            ).exists(),
        )

    def save_vote(self, voter_id, option_id):
        option = Option.objects.select_related("poll__category").get(pk=option_id)
        category = option.poll.category
        try:
            with transaction.atomic():
                Vote.objects.create(
                    user_id=voter_id,
                    edition_id=category.edition_id,
                    category=category,
                    poll=option.poll,
                    option=option,
                )
        except IntegrityError:
            # Two requests passed the rules at the same time; MySQL's unique constraint kept one.
            if Vote.objects.filter(user_id=voter_id, category=category).exists():
                raise VoteRejected("already_voted") from None
            raise

    def list_results(self):
        options_with_votes = Option.objects.annotate(votes_count=Count("votes"))
        polls = (
            Poll.objects.filter(status__in=Poll.PUBLIC_STATUSES)
            .select_related("category__edition")
            .prefetch_related(Prefetch("options", queryset=options_with_votes))
            .order_by("-category__edition__year", "category__name", "title")
        )
        return [
            build_poll_result(
                title=poll.title,
                category=poll.category.name,
                edition_year=poll.category.edition.year,
                is_open=poll.status == Poll.Status.OPEN,
                votes_by_option={option.name: option.votes_count for option in poll.options.all()},
            )
            for poll in polls
        ]
