"""GET /api/categorias/: categories with their public polls and options from MySQL."""
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Category, Poll

PUBLIC_POLL_STATUSES = (Poll.Status.OPEN, Poll.Status.CLOSED)


def serialize_category(category):
    polls = list(category.polls.all())
    return {
        "id": category.pk,
        "nombre": category.name,
        "descripcion": category.description,
        "edicion": {
            "id": category.edition.pk,
            "anio": category.edition.year,
            "nombre": category.edition.name,
        },
        "habilitada": any(poll.status == Poll.Status.OPEN for poll in polls),
        "votaciones": [
            {
                "id": poll.pk,
                "titulo": poll.title,
                "descripcion": poll.description,
                "estado": poll.status,
                "opciones": [
                    {"id": option.pk, "nombre": option.name, "descripcion": option.description}
                    for option in poll.options.all()
                ],
            }
            for poll in polls
        ],
    }


@require_GET
def categories(request):
    public_polls = Poll.objects.filter(status__in=PUBLIC_POLL_STATUSES).prefetch_related("options")
    queryset = (
        Category.objects.select_related("edition")
        .prefetch_related(Prefetch("polls", queryset=public_polls))
        .order_by("-edition__year", "name")
    )
    data = [serialize_category(category) for category in queryset]
    return JsonResponse(
        {"total": len(data), "categorias": data},
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
