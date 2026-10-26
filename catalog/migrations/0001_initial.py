from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Edition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("year", models.PositiveSmallIntegerField(unique=True)),
                ("name", models.CharField(max_length=120)),
            ],
            options={"verbose_name": "edición", "verbose_name_plural": "ediciones", "ordering": ["-year"]},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("edition", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="categories", to="catalog.edition")),
            ],
            options={"verbose_name": "categoría", "verbose_name_plural": "categorías", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("draft", "Borrador"), ("open", "Abierta"), ("closed", "Cerrada")], default="draft", max_length=10)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="polls", to="catalog.category")),
            ],
            options={"verbose_name": "votación", "verbose_name_plural": "votaciones", "ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="catalog.poll")),
            ],
            options={"verbose_name": "opción", "verbose_name_plural": "opciones", "ordering": ["name"]},
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(fields=("edition", "name"), name="unique_category_per_edition"),
        ),
        migrations.AddConstraint(
            model_name="option",
            constraint=models.UniqueConstraint(fields=("poll", "name"), name="unique_option_per_poll"),
        ),
    ]
