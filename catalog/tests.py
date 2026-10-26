from django.core.management import call_command
import os
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.core.management import CommandError, call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Category, Edition, Option, Poll


class CatalogRelationshipTests(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(year=2027, name="Festival Vallenato 2027")
        self.category = Category.objects.create(
            edition=self.edition, name="Rey Vallenato", description="Categoría ficticia"
        )
        self.poll = Poll.objects.create(
            category=self.category, title="Elegir artista favorito", status=Poll.Status.OPEN
        )

    def test_catalog_models_have_declared_related_names_and_status_choices(self):
        option = Option.objects.create(poll=self.poll, name="Artista de muestra")

        self.assertEqual(self.edition.categories.get(), self.category)
        self.assertEqual(self.category.polls.get(), self.poll)
        self.assertEqual(self.poll.options.get(), option)
        self.assertEqual(
            set(Poll.Status.values), {"draft", "open", "closed"}
        )

    def test_edition_year_and_category_name_are_unique_within_edition(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Edition.objects.create(year=2027, name="Duplicate year")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(edition=self.edition, name="Rey Vallenato")

    def test_option_name_is_unique_within_poll(self):
        Option.objects.create(poll=self.poll, name="Artista de muestra")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Option.objects.create(poll=self.poll, name="Artista de muestra")


class PublicCatalogTests(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(year=2027, name="Festival Vallenato 2027")
        self.category = Category.objects.create(
            edition=self.edition, name="Rey Vallenato", description="Categoría ficticia"
        )
        self.open_poll = Poll.objects.create(
            category=self.category, title="Votación abierta", status=Poll.Status.OPEN
        )
        self.closed_poll = Poll.objects.create(
            category=self.category, title="Votación cerrada", status=Poll.Status.CLOSED
        )
        self.draft_poll = Poll.objects.create(
            category=self.category, title="Borrador privado", status=Poll.Status.DRAFT
        )
        Option.objects.create(poll=self.open_poll, name="Opción ficticia")

    def test_home_and_drilldown_render_real_catalog_data(self):
        home = self.client.get(reverse("catalog:home"))
        edition = self.client.get(reverse("catalog:edition", args=[self.edition.pk]))
        category = self.client.get(reverse("catalog:category", args=[self.category.pk]))
        poll = self.client.get(reverse("catalog:poll", args=[self.open_poll.pk]))

        for response in (home, edition, category, poll):
            self.assertEqual(response.status_code, 200)
        self.assertEqual(list(home.context["editions"]), [self.edition])
        self.assertEqual(list(edition.context["categories"]), [self.category])
        self.assertEqual(list(category.context["polls"]), [self.open_poll, self.closed_poll])
        self.assertEqual(list(poll.context["options"]), list(self.open_poll.options.all()))

    def test_draft_poll_is_hidden_from_category_and_direct_url(self):
        category = self.client.get(reverse("catalog:category", args=[self.category.pk]))
        draft = self.client.get(reverse("catalog:poll", args=[self.draft_poll.pk]))

        self.assertNotContains(category, "Borrador privado")
        self.assertEqual(draft.status_code, 404)

    def test_missing_catalog_records_return_404(self):
        self.assertEqual(self.client.get(reverse("catalog:edition", args=[99999])).status_code, 404)
        self.assertEqual(self.client.get(reverse("catalog:category", args=[99999])).status_code, 404)
        self.assertEqual(self.client.get(reverse("catalog:poll", args=[99999])).status_code, 404)


class DemoSeedCommandTests(TestCase):
    def test_seed_is_idempotent_and_does_not_overwrite_edited_rows_or_admin_password(self):
        from django.contrib.auth import get_user_model

        with patch.dict(
            os.environ,
            {"DEMO_ADMIN_USER": "demo-admin", "DEMO_ADMIN_PASSWORD": "seed-password"},
        ):
            admin = get_user_model().objects.create_superuser(
                username="demo-admin", email="admin@example.test", password="custom-password"
            )
            call_command("seed_demo", verbosity=0)
            edition = Edition.objects.get(year=2027)
            edition.name = "Edited by administrator"
            edition.save(update_fields=["name"])
            first_counts = (
                Edition.objects.count(),
                Category.objects.count(),
                Poll.objects.count(),
                Option.objects.count(),
            )

            call_command("seed_demo", verbosity=0)
            edition.refresh_from_db()
            admin.refresh_from_db()

            self.assertEqual(edition.name, "Edited by administrator")
            self.assertEqual(
                first_counts,
                (Edition.objects.count(), Category.objects.count(), Poll.objects.count(), Option.objects.count()),
            )
            self.assertTrue(admin.check_password("custom-password"))
            self.assertTrue(admin.is_staff)
            self.assertTrue(admin.is_superuser)

    def test_seed_creates_admin_from_environment_with_hashed_password(self):
        from django.contrib.auth import get_user_model

        with patch.dict(
            os.environ,
            {"DEMO_ADMIN_USER": "seeded-admin", "DEMO_ADMIN_PASSWORD": "New-admin-pass-2027"},
        ):
            call_command("seed_demo", verbosity=0)

        admin = get_user_model().objects.get(username="seeded-admin")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("New-admin-pass-2027"))
        self.assertNotEqual(admin.password, "New-admin-pass-2027")

    def test_seed_refuses_to_promote_existing_non_staff_username(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_user(username="reserved-user", password="user-password")
        with patch.dict(
            os.environ,
            {"DEMO_ADMIN_USER": "reserved-user", "DEMO_ADMIN_PASSWORD": "New-admin-pass-2027"},
        ):
            with self.assertRaises(CommandError):
                call_command("seed_demo", verbosity=0)

        user.refresh_from_db()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("user-password"))

    def test_seed_requires_demo_admin_environment(self):
        from django.contrib.auth import get_user_model

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(CommandError):
                call_command("seed_demo", verbosity=0)
        self.assertFalse(get_user_model().objects.filter(is_superuser=True).exists())

    def test_static_css_is_available_to_django_staticfiles_finders(self):
        self.assertTrue(finders.find("css/site.css"))

    def test_seed_creates_complete_2027_and_2028_sample_catalog(self):
        with patch.dict(
            os.environ,
            {"DEMO_ADMIN_USER": "seeded-admin", "DEMO_ADMIN_PASSWORD": "New-admin-pass-2027"},
        ):
            call_command("seed_demo", verbosity=0)

        for year in (2027, 2028):
            edition = Edition.objects.get(year=year)
            self.assertTrue(edition.categories.exists())
            self.assertTrue(
                Poll.objects.filter(category__edition=edition, status=Poll.Status.OPEN).exists()
            )
            self.assertTrue(Option.objects.filter(poll__category__edition=edition).exists())
