import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from catalog.models import Category, Edition, Option, Poll


class Command(BaseCommand):
    help = "Create the sample catalog (real artists and songs) without overwriting existing records."

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
                for title, description, status, options in polls:
                    poll, _ = Poll.objects.get_or_create(
                        category=category,
                        title=title,
                        defaults={"description": description, "status": status},
                    )
                    for option_name, option_description in options:
                        Option.objects.get_or_create(
                            poll=poll,
                            name=option_name,
                            defaults={"description": option_description},
                        )
        self.stdout.write(self.style.SUCCESS("Catálogo de demostración disponible."))


def sample_catalog(year):
    """Real artists and songs arranged in the scenarios the demo needs: a category with two
    open subevents, a second open category, a closed category and a hidden draft."""
    open_, closed, draft = Poll.Status.OPEN, Poll.Status.CLOSED, Poll.Status.DRAFT
    return [
        (
            "Íconos del vallenato",
            "Acordeoneros y cantantes que marcaron el género. Un solo voto en toda la categoría.",
            [
                (
                    f"Acordeonero favorito {year}",
                    "Elige al acordeonero que más admiras.",
                    open_,
                    [
                        ("Alfredo Gutiérrez", "Tres veces Rey Vallenato."),
                        ("Egidio Cuadrado", "Acordeonero de Carlos Vives y La Provincia."),
                        ("Israel Romero", "Acordeonero y fundador de El Binomio de Oro."),
                        ("Juancho Rois", "Acordeonero de Diomedes Díaz."),
                    ],
                ),
                (
                    f"Voz favorita {year}",
                    "Subevento de la misma categoría; comparte el límite de un voto.",
                    open_,
                    [
                        ("Diomedes Díaz", "El Cacique de La Junta."),
                        ("Jorge Oñate", "El Jilguero de América."),
                        ("Poncho Zuleta", "Voz de Los Hermanos Zuleta."),
                        ("Silvestre Dangond", "Voz de la nueva generación del vallenato."),
                    ],
                ),
                (f"Nuevos talentos {year}", "Borrador; no aparece en el sitio público.", draft, []),
            ],
        ),
        (
            "Canción vallenata",
            "Clásicos del vallenato con su compositor. Se vota aparte de los íconos.",
            [
                (
                    f"Canción clásica favorita {year}",
                    "Elige la canción que mejor representa al vallenato.",
                    open_,
                    [
                        ("La gota fría", "Compositor: Emiliano Zuleta Baquero."),
                        ("Alicia adorada", "Compositor: Juancho Polo Valencia."),
                        ("Matilde Lina", "Compositor: Leandro Díaz."),
                        ("Pedazo de acordeón", "Compositor: Alejo Durán."),
                        ("Los caminos de la vida", "Compositor: Omar Geles."),
                    ],
                ),
            ],
        ),
        (
            "Homenaje a Rafael Escalona",
            "Canciones de Rafael Escalona, uno de los fundadores del festival.",
            [
                (
                    f"Canción de Escalona favorita {year}",
                    "Votación cerrada; ya no recibe votos.",
                    closed,
                    [
                        ("La casa en el aire", "Compositor: Rafael Escalona."),
                        ("El testamento", "Compositor: Rafael Escalona."),
                        ("Jaime Molina", "Compositor: Rafael Escalona."),
                        ("La custodia de Badillo", "Compositor: Rafael Escalona."),
                    ],
                ),
            ],
        ),
    ]
