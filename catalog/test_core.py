"""Core tests: the hexagon runs without Django models, HTTP or MySQL."""
import ast
from pathlib import Path

from django.test import SimpleTestCase

from .core.domain import VoteFacts, VoteRejected, build_poll_result, check_vote
from .core.services import VotingService


class InMemoryVoteRepository:
    """Second adapter for the same port: proves the core does not depend on MySQL."""

    def __init__(self, facts):
        self.facts = facts
        self.saved = []

    def get_vote_facts(self, voter_id, poll_id, option_id):
        return self.facts

    def save_vote(self, voter_id, option_id):
        self.saved.append((voter_id, option_id))

    def list_results(self):
        return [build_poll_result("Acordeonero", "Rey Vallenato", 2027, True, {"A": 1})]


VALID = VoteFacts(poll_is_open=True, option_belongs_to_poll=True, already_voted_in_category=False)


class VoteRulesTests(SimpleTestCase):
    def test_each_broken_rule_has_its_own_rejection(self):
        cases = [
            (VoteFacts(False, True, False), "poll_not_open"),
            (VoteFacts(True, False, False), "option_mismatch"),
            (VoteFacts(True, True, True), "already_voted"),
            (VoteFacts(False, False, True), "poll_not_open"),
        ]
        for facts, expected in cases:
            with self.subTest(facts=facts), self.assertRaises(VoteRejected) as rejection:
                check_vote(facts)
            self.assertEqual(rejection.exception.code, expected)

    def test_valid_vote_passes_every_rule(self):
        self.assertIsNone(check_vote(VALID))

    def test_rejection_message_is_the_text_shown_to_the_voter(self):
        self.assertEqual(
            str(VoteRejected("already_voted")), "Ya registraste un voto en esta categoría."
        )


class PollResultTests(SimpleTestCase):
    def test_counts_are_ranked_with_rounded_percentages(self):
        result = build_poll_result("Final", "Piquería", 2028, False, {"B": 1, "A": 2, "C": 0})

        self.assertEqual(result.total_votes, 3)
        self.assertEqual(
            [(o.name, o.votes, o.percent) for o in result.options],
            [("A", 2, 67), ("B", 1, 33), ("C", 0, 0)],
        )

    def test_ties_are_ordered_by_name(self):
        result = build_poll_result("Final", "Piquería", 2028, True, {"Zeta": 1, "Alfa": 1})
        self.assertEqual([o.name for o in result.options], ["Alfa", "Zeta"])

    def test_poll_without_votes_shows_zero_percent(self):
        result = build_poll_result("Final", "Piquería", 2028, True, {"A": 0})
        self.assertEqual((result.total_votes, result.options[0].percent), (0, 0))


class VotingServiceTests(SimpleTestCase):
    def test_valid_vote_is_stored_through_the_port(self):
        repository = InMemoryVoteRepository(VALID)
        VotingService(repository).cast(voter_id=7, poll_id=1, option_id=3)
        self.assertEqual(repository.saved, [(7, 3)])

    def test_rejected_vote_is_never_stored(self):
        repository = InMemoryVoteRepository(VoteFacts(True, True, True))
        with self.assertRaises(VoteRejected):
            VotingService(repository).cast(voter_id=7, poll_id=1, option_id=3)
        self.assertEqual(repository.saved, [])

    def test_anonymous_voter_is_rejected_before_reading_the_database(self):
        repository = InMemoryVoteRepository(facts=None)
        with self.assertRaises(VoteRejected) as rejection:
            VotingService(repository).cast(voter_id=None, poll_id=1, option_id=3)
        self.assertEqual(rejection.exception.code, "not_authenticated")
        self.assertEqual(repository.saved, [])

    def test_check_validates_without_storing(self):
        repository = InMemoryVoteRepository(VALID)
        VotingService(repository).check(voter_id=7, poll_id=1, option_id=3)
        self.assertEqual(repository.saved, [])

    def test_results_come_from_the_repository(self):
        results = VotingService(InMemoryVoteRepository(VALID)).results()
        self.assertEqual([(r.title, r.total_votes) for r in results], [("Acordeonero", 1)])


class ArchitectureTests(SimpleTestCase):
    def test_core_never_imports_django_or_outer_layers(self):
        core = Path(__file__).parent / "core"
        forbidden = ("django", "catalog.models", "catalog.repository", "catalog.views")
        for source in core.glob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [("." * node.level) + (node.module or "")]
                else:
                    continue
                for name in names:
                    with self.subTest(file=source.name, module=name):
                        self.assertFalse(name.startswith(forbidden))
                        self.assertNotIn(name, ("..models", "..repository", "..views"))
