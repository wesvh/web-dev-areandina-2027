from django.db import connections
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Edition, Poll


def home(request):
    editions = Edition.objects.prefetch_related("categories").all()
    return render(request, "catalog/home.html", {"editions": editions})


def edition_detail(request, pk):
    edition = get_object_or_404(Edition, pk=pk)
    categories = edition.categories.prefetch_related("polls").all()
    return render(
        request,
        "catalog/edition_detail.html",
        {"edition": edition, "categories": categories},
    )


def category_detail(request, pk):
    category = get_object_or_404(Category.objects.select_related("edition"), pk=pk)
    polls = category.polls.filter(status__in=[Poll.Status.OPEN, Poll.Status.CLOSED])
    return render(
        request,
        "catalog/category_detail.html",
        {"category": category, "polls": polls},
    )


def poll_detail(request, pk):
    poll = get_object_or_404(
        Poll.objects.select_related("category", "category__edition").prefetch_related("options"),
        pk=pk,
        status__in=[Poll.Status.OPEN, Poll.Status.CLOSED],
    )
    return render(request, "catalog/poll_detail.html", {"poll": poll, "options": poll.options.all()})


def health(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})
