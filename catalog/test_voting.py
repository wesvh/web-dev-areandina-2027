import json
import threading

from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from .models import Category, Edition, Option, Poll, Vote
from .voting import VoteRejected, cast_vote


def build_catalog():
    """Fictional catalog: one category with two open subevents, a second open
    category, a closed category and a draft poll."""
    edition = Edition.objects.create(year=2027, name="Festival Vallenato 2027")
    rey = Category.objects.create(edition=edition, name="Rey Vallenato")
    cancion = Category.objects.create(edition=edition, name="Canción inédita")
    piqueria = Category.objects.create(edition=edition, name="Piquería")
    rey_main = Poll.objects.create(category=rey, title="Acordeonero", status=Poll.Status.OPEN)
    rey_sub = Poll.objects.create(category=rey, title="Ronda final", status=Poll.Status.OPEN)
    cancion_poll = Poll.objects.create(
        category=cancion, title="Canción favorita", status=Poll.Status.OPEN
    )
    closed_poll = Poll.objects.create(
        category=piqueria, title="Piquería cerrada", status=Poll.Status.CLOSED
    )
    draft_poll = Poll.objects.create(category=rey, title="Borrador", status=Poll.Status.DRAFT)
    return {
        "edition": edition,
        "rey": rey,
        "cancion": cancion,
        "rey_main": rey_main,
        "rey_sub": rey_sub,
        "cancion_poll": cancion_poll,
        "closed_poll": closed_poll,
        "draft_poll": draft_poll,
        "rey_a": Option.objects.create(poll=rey_main, name="Acordeonero A"),
        "rey_b": Option.objects.create(poll=rey_main, name="Acordeonero B"),
        "rey_sub_a": Option.objects.create(poll=rey_sub, name="Finalista A"),
        "cancion_a": Option.objects.create(poll=cancion_poll, name="Canción A"),
        "closed_a": Option.objects.create(poll=closed_poll, name="Piquero A"),
        "draft_a": Option.objects.create(poll=draft_poll, name="Oculta A"),
    }


class VotingFlowTests(TestCase):
    def setUp(self):
        self.c = build_catalog()
        self.user = get_user_model().objects.create_user("votante", password="Clave-segura-2027")
        self.client.force_login(self.user)

    def vote_url(self, poll):
        return reverse("catalog:vote", args=[poll.pk])

    def confirm_vote(self, poll, option):
        return self.client.post(
            self.vote_url(poll), {"option": option.pk, "confirm": "1"}, follow=True
        )

    def test_cp01_valid_vote_requires_confirmation_then_persists_derived_relations(self):
        selection = self.client.post(self.vote_url(self.c["rey_main"]), {"option": self.c["rey_a"].pk})

        self.assertEqual(selection.status_code, 200)
        self.assertContains(selection, "Confirmar voto")
        self.assertContains(selection, "Acordeonero A")
        self.assertFalse(Vote.objects.exists())

        response = self.confirm_vote(self.c["rey_main"], self.c["rey_a"])

        vote = Vote.objects.get()
        self.assertEqual(
            (vote.user, vote.edition, vote.category, vote.poll, vote.option),
            (self.user, self.c["edition"], self.c["rey"], self.c["rey_main"], self.c["rey_a"]),
        )
        self.assertRedirects(response, reverse("catalog:my-votes"))
        self.assertContains(response, "Voto registrado")

    def test_cp02_second_vote_in_same_category_is_rejected_for_other_option_and_subevent(self):
        self.confirm_vote(self.c["rey_main"], self.c["rey_a"])

        other_option = self.confirm_vote(self.c["rey_main"], self.c["rey_b"])
        other_subevent = self.confirm_vote(self.c["rey_sub"], self.c["rey_sub_a"])

        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.get().option, self.c["rey_a"])
        self.assertContains(other_option, "Ya registraste un voto en esta categoría")
        self.assertContains(other_subevent, "Ya registraste un voto en esta categoría")

    def test_cp03_vote_in_a_different_category_is_allowed(self):
        self.confirm_vote(self.c["rey_main"], self.c["rey_a"])
        self.confirm_vote(self.c["cancion_poll"], self.c["cancion_a"])

        self.assertEqual(
            set(Vote.objects.values_list("category__name", flat=True)),
            {"Rey Vallenato", "Canción inédita"},
        )

    def test_cp04_anonymous_user_is_sent_to_login_and_nothing_is_stored(self):
        self.client.logout()

        response = self.client.post(
            self.vote_url(self.c["rey_main"]), {"option": self.c["rey_a"].pk, "confirm": "1"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith(reverse("accounts:login")))
        self.assertFalse(Vote.objects.exists())

    def test_cp05_closed_poll_rejects_vote_and_draft_poll_is_not_found(self):
        closed = self.confirm_vote(self.c["closed_poll"], self.c["closed_a"])
        draft = self.client.post(
            self.vote_url(self.c["draft_poll"]), {"option": self.c["draft_a"].pk, "confirm": "1"}
        )

        self.assertContains(closed, "La votación no está habilitada")
        self.assertEqual(draft.status_code, 404)
        self.assertFalse(Vote.objects.exists())

    def test_cp06_option_from_another_category_is_rejected(self):
        response = self.confirm_vote(self.c["rey_main"], self.c["cancion_a"])

        self.assertContains(response, "La opción no pertenece a esta votación")
        self.assertFalse(Vote.objects.exists())

    def test_cp07_my_votes_lists_only_the_users_own_voted_categories(self):
        self.confirm_vote(self.c["rey_main"], self.c["rey_a"])
        other = get_user_model().objects.create_user("otro", password="Clave-segura-2027")
        cast_vote(other, self.c["cancion_poll"], self.c["cancion_a"].pk)

        response = self.client.get(reverse("catalog:my-votes"))

        self.assertContains(response, "Rey Vallenato")
        self.assertContains(response, "Acordeonero A")
        self.assertNotContains(response, "Canción A")

    def test_my_votes_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("catalog:my-votes"))
        self.assertEqual(response.status_code, 302)

    def test_vote_endpoint_rejects_get(self):
        response = self.client.get(self.vote_url(self.c["rey_main"]))
        self.assertEqual(response.status_code, 405)

    def test_vote_without_csrf_token_is_forbidden(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)

        response = csrf_client.post(
            self.vote_url(self.c["rey_main"]), {"option": self.c["rey_a"].pk, "confirm": "1"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Vote.objects.exists())

    def test_poll_page_shows_vote_form_and_existing_vote_notice(self):
        form_page = self.client.get(reverse("catalog:poll", args=[self.c["rey_main"].pk]))
        self.assertContains(form_page, 'name="option"')

        self.confirm_vote(self.c["rey_main"], self.c["rey_a"])
        voted_page = self.client.get(reverse("catalog:poll", args=[self.c["rey_sub"].pk]))
        self.assertContains(voted_page, "Ya votaste en esta categoría")
        self.assertNotContains(voted_page, 'name="option"')


class VoteStorageTests(TestCase):
    def test_database_rejects_duplicate_vote_for_user_category_and_edition(self):
        c = build_catalog()
        user = get_user_model().objects.create_user("votante", password="Clave-segura-2027")
        Vote.objects.create(
            user=user, edition=c["edition"], category=c["rey"], poll=c["rey_main"], option=c["rey_a"]
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            Vote.objects.create(
                user=user, edition=c["edition"], category=c["rey"], poll=c["rey_sub"],
                option=c["rey_sub_a"],
            )


class AdminVoteTests(TestCase):
    def setUp(self):
        self.c = build_catalog()
        self.voter = get_user_model().objects.create_user("votante", password="Clave-segura-2027")
        cast_vote(self.voter, self.c["rey_main"], self.c["rey_a"].pk)
        self.admin = get_user_model().objects.create_superuser("admin", password="Clave-admin-2027")

    def test_cp08_admin_vote_list_matches_database_and_is_read_only(self):
        self.client.force_login(self.admin)

        listing = self.client.get(reverse("admin:catalog_vote_changelist"))
        add = self.client.get(reverse("admin:catalog_vote_add"))

        self.assertContains(listing, "votante")
        self.assertContains(listing, "Acordeonero A")
        self.assertContains(listing, "Rey Vallenato")
        self.assertEqual(add.status_code, 403)

    def test_regular_user_cannot_open_admin_vote_list(self):
        self.client.force_login(self.voter)
        response = self.client.get(reverse("admin:catalog_vote_changelist"))
        self.assertEqual(response.status_code, 302)


class ConcurrentVoteTests(TransactionTestCase):
    def test_cp09_simultaneous_requests_store_a_single_vote(self):
        c = build_catalog()
        user = get_user_model().objects.create_user("votante", password="Clave-segura-2027")
        attempts = [(c["rey_main"], c["rey_a"]), (c["rey_sub"], c["rey_sub_a"])] * 3
        barrier = threading.Barrier(len(attempts))
        outcomes = []

        def attempt(poll, option):
            try:
                barrier.wait()
                cast_vote(user, poll, option.pk)
                outcomes.append("stored")
            except VoteRejected as rejection:
                outcomes.append(rejection.code)
            finally:
                connection.close()

        threads = [threading.Thread(target=attempt, args=pair) for pair in attempts]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(Vote.objects.filter(user=user, category=c["rey"]).count(), 1)
        self.assertEqual(outcomes.count("stored"), 1)
        self.assertEqual(outcomes.count("already_voted"), len(attempts) - 1)


class CategoriesApiTests(TestCase):
    def setUp(self):
        self.c = build_catalog()

    def test_cp10_get_returns_valid_json_with_categories_and_options_from_database(self):
        response = self.client.get("/api/categorias/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = json.loads(response.content)
        categories = {item["nombre"]: item for item in payload["categorias"]}
        self.assertEqual(payload["total"], 3)
        self.assertEqual(categories["Rey Vallenato"]["edicion"]["anio"], 2027)
        self.assertTrue(categories["Rey Vallenato"]["habilitada"])
        self.assertFalse(categories["Piquería"]["habilitada"])
        rey_polls = {poll["titulo"]: poll for poll in categories["Rey Vallenato"]["votaciones"]}
        self.assertEqual(set(rey_polls), {"Acordeonero", "Ronda final"})
        self.assertEqual(
            [option["nombre"] for option in rey_polls["Acordeonero"]["opciones"]],
            ["Acordeonero A", "Acordeonero B"],
        )
        self.assertEqual(rey_polls["Acordeonero"]["estado"], "open")

    def test_api_excludes_draft_polls(self):
        payload = self.client.get("/api/categorias/").json()
        names = [
            option["nombre"]
            for category in payload["categorias"]
            for poll in category["votaciones"]
            for option in poll["opciones"]
        ]
        self.assertNotIn("Oculta A", names)

    def test_api_uses_constant_number_of_queries(self):
        with self.assertNumQueries(3):
            self.client.get("/api/categorias/")

    def test_api_only_accepts_get(self):
        self.assertEqual(self.client.post("/api/categorias/").status_code, 405)
