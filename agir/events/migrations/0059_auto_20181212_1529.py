# Generated by Django 2.1.4 on 2018-12-12 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0058_auto_20181205_1844")]

    operations = [
        migrations.AlterField(
            model_name="eventsubtype",
            name="external_help_text",
            field=models.TextField(
                blank=True,
                verbose_name="Phrase d'explication pour rejoindre le groupe ou l'évènement",
            ),
        )
    ]
