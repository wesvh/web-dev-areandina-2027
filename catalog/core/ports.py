"""Ports: what the core needs from the outside, described as an interface."""
from typing import Protocol

from .domain import PollResult, VoteFacts


class VoteRepository(Protocol):
    """Output port for vote storage. The MySQL adapter is catalog/repository.py."""

    def get_vote_facts(self, voter_id: int, poll_id: int, option_id: int) -> VoteFacts:
        """Read what the rules need to accept or reject a vote."""

    def save_vote(self, voter_id: int, option_id: int) -> None:
        """Store the vote. Raise VoteRejected("already_voted") if one already exists."""

    def list_results(self) -> list[PollResult]:
        """Count the stored votes of every public poll."""
