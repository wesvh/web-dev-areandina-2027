"""Domain: the voting rules of the festival, written in plain Python."""
from dataclasses import dataclass


class VoteRejected(Exception):
    """A vote that breaks a rule. `code` names the rule; the message is shown to the voter."""

    MESSAGES = {
        "not_authenticated": "Debes iniciar sesión para votar.",
        "option_required": "Selecciona una opción antes de continuar.",
        "poll_not_open": "La votación no está habilitada para recibir votos.",
        "option_mismatch": "La opción no pertenece a esta votación.",
        "already_voted": "Ya registraste un voto en esta categoría.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.MESSAGES[code])


@dataclass(frozen=True)
class VoteFacts:
    """What the database knows about one vote attempt."""

    poll_is_open: bool
    option_belongs_to_poll: bool
    already_voted_in_category: bool


def check_vote(facts):
    """Raise VoteRejected if the vote breaks a rule; return nothing if it is valid."""
    if not facts.poll_is_open:
        raise VoteRejected("poll_not_open")
    if not facts.option_belongs_to_poll:
        raise VoteRejected("option_mismatch")
    if facts.already_voted_in_category:
        raise VoteRejected("already_voted")


@dataclass(frozen=True)
class OptionResult:
    name: str
    votes: int
    percent: int


@dataclass(frozen=True)
class PollResult:
    title: str
    category: str
    edition_year: int
    is_open: bool
    total_votes: int
    options: tuple


def build_poll_result(title, category, edition_year, is_open, votes_by_option):
    """Turn raw counts {option name: votes} into a result ordered from most to least voted."""
    total = sum(votes_by_option.values())
    ranking = sorted(votes_by_option.items(), key=lambda item: (-item[1], item[0]))
    options = tuple(
        OptionResult(name, votes, round(votes * 100 / total) if total else 0)
        for name, votes in ranking
    )
    return PollResult(title, category, edition_year, is_open, total, options)
