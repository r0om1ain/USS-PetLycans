import hashlib

import django.db.models.deletion
from django.db import migrations, models


def coords_depuis_nom(nom: str) -> tuple[float, float, float]:
    digest = hashlib.sha256(nom.encode("utf-8")).digest()
    coords = []
    for i in range(3):
        chunk = int.from_bytes(digest[i * 4 : (i + 1) * 4], "big")
        coords.append((chunk / 0xFFFFFFFF) * 2000 - 1000)
    return coords[0], coords[1], coords[2]


def migrate_destinations_to_lieux(apps, schema_editor):
    Lieu = apps.get_model("space_agency", "Lieu")
    Mission = apps.get_model("space_agency", "Mission")
    cache = {}
    for mission in Mission.objects.all():
        nom = mission.destination_old
        if nom not in cache:
            x, y, z = coords_depuis_nom(nom)
            lieu, _ = Lieu.objects.get_or_create(
                nom=nom, defaults={"x": x, "y": y, "z": z}
            )
            cache[nom] = lieu
        mission.destination = cache[nom]
        mission.save(update_fields=["destination"])


def reverse_destinations(apps, schema_editor):
    Mission = apps.get_model("space_agency", "Mission")
    for mission in Mission.objects.select_related("destination").all():
        mission.destination_old = mission.destination.nom
        mission.save(update_fields=["destination_old"])


class Migration(migrations.Migration):

    dependencies = [
        ("space_agency", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lieu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                ("x", models.FloatField(blank=True, null=True)),
                ("y", models.FloatField(blank=True, null=True)),
                ("z", models.FloatField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Lieu",
                "verbose_name_plural": "Lieux",
            },
        ),
        migrations.AlterModelOptions(
            name="vaisseau",
            options={
                "verbose_name": "Vaisseau",
                "verbose_name_plural": "Vaisseaux",
            },
        ),
        migrations.RenameField(
            model_name="mission",
            old_name="destination",
            new_name="destination_old",
        ),
        migrations.AddField(
            model_name="mission",
            name="destination",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="missions",
                to="space_agency.lieu",
            ),
        ),
        migrations.RunPython(migrate_destinations_to_lieux, reverse_destinations),
        migrations.AlterField(
            model_name="mission",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="missions",
                to="space_agency.lieu",
            ),
        ),
        migrations.RemoveField(
            model_name="mission",
            name="destination_old",
        ),
    ]
