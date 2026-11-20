"""Use cases: the actions the web layer can ask the core to perform."""
from .domain import VoteRejected, check_vote


class VotingService:
    """Receives any VoteRepository (input port of the hexagon)."""

    def __init__(self, repository):
        self.repository = repository

    def check(self, voter_id, poll_id, option_id):
        """Validate a vote without storing it. Used by the confirmation page."""
        if voter_id is None:
            raise VoteRejected("not_authenticated")
        check_vote(self.repository.get_vote_facts(voter_id, poll_id, option_id))

    def cast(self, voter_id, poll_id, option_id):
        """Validate and store a vote."""
        self.check(voter_id, poll_id, option_id)
        self.repository.save_vote(voter_id, option_id)

    def results(self):
        """Vote counts per option for every public poll."""
        return self.repository.list_results()
