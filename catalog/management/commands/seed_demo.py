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
            category, _ = Category.objects.get_or_create(
                edition=edition,
                name="Rey Vallenato - muestra ficticia",
                defaults={"description": "Categoría de demostración; participantes ficticios."},
            )
            open_poll, _ = Poll.objects.get_or_create(
                category=category,
                title=f"Artista favorito {year} - muestra",
                defaults={
                    "description": "Votación ficticia para demostración; no registra votos.",
                    "status": Poll.Status.OPEN,
                },
            )
            Poll.objects.get_or_create(
                category=category,
                title=f"Votación borrador {year} - muestra",
                defaults={
                    "description": "Borrador de demostración no visible en el catálogo público.",
                    "status": Poll.Status.DRAFT,
                },
            )
            for name in ("Acordeón de muestra", "Compositor de muestra"):
                Option.objects.get_or_create(
                    poll=open_poll,
                    name=f"{name} {year}",
                    defaults={"description": "Opción ficticia de demostración."},
                )
        self.stdout.write(self.style.SUCCESS("Catálogo de demostración disponible."))
