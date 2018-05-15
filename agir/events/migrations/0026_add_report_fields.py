# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 18:49
from __future__ import unicode_literals

from django.db import migrations
from agir.lib import models as lib_models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20171205_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='report_content',
            field=lib_models.DescriptionField(blank=True, help_text="Ajoutez un compte-rendu de votre événement. N'hésitez pas à inclure des photos.", verbose_name="compte-rendu de l'événement"),
        ),
        migrations.AddField(
            model_name='event',
            name='report_image',
            field=stdimage.models.StdImageField(blank=True, help_text='Cette image apparaîtra en tête de votre compte-rendu, et dans les partages que vous ferez du compte-rendu sur les réseaux sociaux.', upload_to='', verbose_name='image de couverture'),
        ),
    ]