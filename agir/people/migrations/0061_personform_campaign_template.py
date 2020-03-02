# Generated by Django 2.2.10 on 2020-02-18 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("nuntius", "0017_campaign_utm_name"),
        ("people", "0060_personform_segment"),
    ]

    operations = [
        migrations.AddField(
            model_name="personform",
            name="campaign_template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="nuntius.Campaign",
                verbose_name="Créer une campagne à partir de ce modèle",
            ),
        )
    ]