# Generated by Django 3.1.5 on 2021-01-21 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data_france", "0015_recherche_elus_municipaux"),
        ("elus", "0016_mandatmunicipal_reference"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mandatdepartemental",
            name="statut",
            field=models.CharField(
                choices=[
                    ("INC", "Mandat à vérifier (ajouté côté admin)"),
                    ("DEM", "Mandat à vérifier (ajouté par la personne elle-même)"),
                    ("IMP", "Importé par une opération automatique"),
                    ("FXP", "Faux-positif dans une opération d'import"),
                    ("INS", "Mandat vérifié"),
                ],
                default="INC",
                help_text="Indique la qualité de l'information sur cet⋅te élu⋅e, indépendamment des questions politiques et de son appartenance au réseau des élus. Une valeur « Vérifié » signifie que : 1) il a été vérifié que le mandat existe réellement et 2) le compte éventuellement associé appartient bien à la personne élue.",
                max_length=3,
                verbose_name="Statut",
            ),
        ),
        migrations.AlterField(
            model_name="mandatmunicipal",
            name="reference",
            field=models.ForeignKey(
                blank=True,
                help_text="La fiche correspondant à cet élu dans le Répertoire National des Élus",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_france.elumunicipal",
                verbose_name="Référence dans le RNE",
            ),
        ),
        migrations.AlterField(
            model_name="mandatmunicipal",
            name="statut",
            field=models.CharField(
                choices=[
                    ("INC", "Mandat à vérifier (ajouté côté admin)"),
                    ("DEM", "Mandat à vérifier (ajouté par la personne elle-même)"),
                    ("IMP", "Importé par une opération automatique"),
                    ("FXP", "Faux-positif dans une opération d'import"),
                    ("INS", "Mandat vérifié"),
                ],
                default="INC",
                help_text="Indique la qualité de l'information sur cet⋅te élu⋅e, indépendamment des questions politiques et de son appartenance au réseau des élus. Une valeur « Vérifié » signifie que : 1) il a été vérifié que le mandat existe réellement et 2) le compte éventuellement associé appartient bien à la personne élue.",
                max_length=3,
                verbose_name="Statut",
            ),
        ),
        migrations.AlterField(
            model_name="mandatregional",
            name="statut",
            field=models.CharField(
                choices=[
                    ("INC", "Mandat à vérifier (ajouté côté admin)"),
                    ("DEM", "Mandat à vérifier (ajouté par la personne elle-même)"),
                    ("IMP", "Importé par une opération automatique"),
                    ("FXP", "Faux-positif dans une opération d'import"),
                    ("INS", "Mandat vérifié"),
                ],
                default="INC",
                help_text="Indique la qualité de l'information sur cet⋅te élu⋅e, indépendamment des questions politiques et de son appartenance au réseau des élus. Une valeur « Vérifié » signifie que : 1) il a été vérifié que le mandat existe réellement et 2) le compte éventuellement associé appartient bien à la personne élue.",
                max_length=3,
                verbose_name="Statut",
            ),
        ),
    ]