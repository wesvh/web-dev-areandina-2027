from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse


class RegistrationAndAuthenticationTests(TestCase):
    def test_registration_creates_non_staff_user_with_hashed_password(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "vallenato-fan",
                "password1": "Str0ng!Password-2027",
                "password2": "Str0ng!Password-2027",
            },
        )

        self.assertRedirects(response, reverse("catalog:home"))
        user = get_user_model().objects.get(username="vallenato-fan")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("Str0ng!Password-2027"))
        self.assertNotEqual(user.password, "Str0ng!Password-2027")

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(username="taken", password="existing")

        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "taken",
                "password1": "Str0ng!Password-2027",
                "password2": "Str0ng!Password-2027",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.filter(username="taken").count(), 1)
        self.assertIn("username", response.context["form"].errors)

    def test_login_rejects_external_next_url(self):
        user = get_user_model().objects.create_user(
            username="member", password="Str0ng!Password-2027"
        )

        response = self.client.post(
            reverse("accounts:login") + "?next=https://evil.example/",
            {"username": user.username, "password": "Str0ng!Password-2027"},
        )

        self.assertRedirects(response, reverse("catalog:home"))

    def test_registration_rejects_external_next_url(self):
        response = self.client.post(
            reverse("accounts:register") + "?next=//evil.example/",
            {
                "username": "safe-member",
                "password1": "Str0ng!Password-2027",
                "password2": "Str0ng!Password-2027",
            },
        )

        self.assertRedirects(response, reverse("catalog:home"))

    def test_logout_requires_post(self):
        get_user_model().objects.create_user(
            username="member", password="Str0ng!Password-2027"
        )
        self.client.login(username="member", password="Str0ng!Password-2027")

        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_logout_ends_session(self):
        get_user_model().objects.create_user(
            username="member", password="Str0ng!Password-2027"
        )
        self.client.login(username="member", password="Str0ng!Password-2027")

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("catalog:home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registration_enforces_csrf(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            reverse("accounts:register"),
            {
                "username": "csrf-member",
                "password1": "Str0ng!Password-2027",
                "password2": "Str0ng!Password-2027",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(get_user_model().objects.filter(username="csrf-member").exists())

    def test_login_enforces_csrf(self):
        user = get_user_model().objects.create_user(
            username="csrf-login", password="Str0ng!Password-2027"
        )
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            reverse("accounts:login"),
            {"username": user.username, "password": "Str0ng!Password-2027"},
        )

        self.assertEqual(response.status_code, 403)


class AdminAccessTests(TestCase):
    def test_non_staff_cannot_access_admin(self):
        get_user_model().objects.create_user(username="member", password="password")
        self.client.login(username="member", password="password")

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response["Location"])


class HealthEndpointTests(TestCase):
    def test_health_endpoint_checks_database_and_returns_json(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})


@override_settings(ALLOWED_HOSTS=["testserver"])
class HostSettingsTest(TestCase):
    def test_test_host_is_accepted(self):
        self.assertEqual(self.client.get(reverse("catalog:home")).status_code, 200)
