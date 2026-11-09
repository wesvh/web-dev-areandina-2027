"""Server-side voting rules: one vote per user, category and edition."""
from django.db import IntegrityError, transaction

from .models import Option, Poll, Vote


class VoteRejected(Exception):
    MESSAGES = {
        "not_authenticated": "Debes iniciar sesión para votar.",
        "poll_not_open": "La votación no está habilitada para recibir votos.",
        "option_required": "Selecciona una opción antes de continuar.",
        "option_mismatch": "La opción no pertenece a esta votación.",
        "already_voted": "Ya registraste un voto en esta categoría.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.MESSAGES[code])


def validate_vote(user, poll, option_id):
    """Return the option if the vote is acceptable; raise VoteRejected otherwise."""
    if not user.is_authenticated:
        raise VoteRejected("not_authenticated")
    if poll.status != Poll.Status.OPEN:
        raise VoteRejected("poll_not_open")
    option = (
        Option.objects.select_related("poll__category__edition")
        .filter(pk=option_id, poll=poll)
        .first()
    )
    if option is None:
        raise VoteRejected("option_mismatch")
    if Vote.objects.filter(user=user, category_id=poll.category_id).exists():
        raise VoteRejected("already_voted")
    return option


def cast_vote(user, poll, option_id):
    """Store a vote; relations are derived from the option, never from the client."""
    option = validate_vote(user, poll, option_id)
    category = option.poll.category
    try:
        with transaction.atomic():
            return Vote.objects.create(
                user=user,
                edition=category.edition,
                category=category,
                poll=option.poll,
                option=option,
            )
    except IntegrityError as error:
        # A concurrent request stored the vote first; the unique constraint keeps one.
        if Vote.objects.filter(user=user, category=category).exists():
            raise VoteRejected("already_voted") from error
        raise
