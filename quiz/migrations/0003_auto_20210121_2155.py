# Generated by Django 3.1.5 on 2021-01-21 21:55

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210121_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
    ]