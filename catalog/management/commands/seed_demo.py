import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from catalog.models import Category, Edition, Option, Poll


class Command(BaseCommand):
    help = "Create fictional sample catalog entries without overwriting existing records."

    def handle(self, *args, **options):
        admin_username = os.environ.get("DEMO_ADMIN_USER")
        admin_password = os.environ.get("DEMO_ADMIN_PASSWORD")
        if not admin_username or not admin_password:
            raise CommandError("DEMO_ADMIN_USER and DEMO_ADMIN_PASSWORD are required.")

        user_model = get_user_model()
        admin, created = user_model.objects.get_or_create(
            username=admin_username,
            defaults={"is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password(admin_password)
            admin.save(update_fields=["password"])
        elif not (admin.is_staff and admin.is_superuser):
            raise CommandError(
                "Configured demo admin already exists without staff and superuser privileges."
            )

        for year in (2027, 2028):
            edition, _ = Edition.objects.get_or_create(
                year=year, defaults={"name": f"Festival Vallenato {year}"}
            )
            for category_name, category_description, polls in sample_catalog(year):
                category, _ = Category.objects.get_or_create(
                    edition=edition,
                    name=category_name,
                    defaults={"description": category_description},
                )
                for title, description, status, option_names in polls:
                    poll, _ = Poll.objects.get_or_create(
                        category=category,
                        title=title,
                        defaults={"description": description, "status": status},
                    )
                    for option_name in option_names:
                        Option.objects.get_or_create(
                            poll=poll,
                            name=option_name,
                            defaults={"description": "Opción ficticia de demostración."},
                        )
        self.stdout.write(self.style.SUCCESS("Catálogo de demostración disponible."))


def sample_catalog(year):
    """Fictional voting scenarios: multi-subevent category, second open category,
    closed category and a hidden draft."""
    open_, closed, draft = Poll.Status.OPEN, Poll.Status.CLOSED, Poll.Status.DRAFT
    return [
        (
            "Rey Vallenato - muestra ficticia",
            "Categoría de demostración; participantes ficticios.",
            [
                (
                    f"Artista favorito {year} - muestra",
                    "Votación ficticia de demostración; un voto por usuario en esta categoría.",
                    open_,
                    [f"Acordeón de muestra {year}", f"Compositor de muestra {year}"],
                ),
                (
                    f"Ronda final {year} - muestra",
                    "Subevento ficticio de la misma categoría; comparte el límite de un voto.",
                    open_,
                    [f"Finalista ficticio A {year}", f"Finalista ficticio B {year}"],
                ),
                (
                    f"Votación borrador {year} - muestra",
                    "Borrador de demostración no visible en el catálogo público.",
                    draft,
                    [],
                ),
            ],
        ),
        (
            "Canción inédita - muestra ficticia",
            "Segunda categoría de demostración; permite votar de forma independiente.",
            [
                (
                    f"Canción favorita {year} - muestra",
                    "Votación ficticia de demostración.",
                    open_,
                    [f"Canción de muestra A {year}", f"Canción de muestra B {year}"],
                ),
            ],
        ),
        (
            "Piquería - muestra ficticia",
            "Categoría de demostración con la votación cerrada.",
            [
                (
                    f"Piquería {year} - muestra cerrada",
                    "Votación cerrada; no recibe votos.",
                    closed,
                    [f"Piquero de muestra A {year}", f"Piquero de muestra B {year}"],
                ),
            ],
        ),
    ]
