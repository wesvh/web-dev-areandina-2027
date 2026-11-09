from django.conf import settings
from django.db import models


class Edition(models.Model):
    year = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ["-year"]
        verbose_name = "edición"
        verbose_name_plural = "ediciones"

    def __str__(self):
        return self.name


class Category(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["edition", "name"], name="unique_category_per_edition")
        ]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return f"{self.name} ({self.edition.year})"


class Poll(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        OPEN = "open", "Abierta"
        CLOSED = "closed", "Cerrada"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="polls")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ["title"]
        verbose_name = "votación"
        verbose_name_plural = "votaciones"

    def __str__(self):
        return self.title


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["poll", "name"], name="unique_option_per_poll")
        ]
        verbose_name = "opción"
        verbose_name_plural = "opciones"

    def __str__(self):
        return self.name


class Vote(models.Model):
    """One vote per user, category and edition, enforced by the database."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes"
    )
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT, related_name="votes")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="votes")
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT, related_name="votes")
    option = models.ForeignKey(Option, on_delete=models.PROTECT, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "edition"],
                name="unique_vote_per_user_category_edition",
            )
        ]
        verbose_name = "voto"
        verbose_name_plural = "votos"

    def __str__(self):
        return f"{self.user} → {self.option} ({self.category})"
