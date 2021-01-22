# Generated by Django 3.1.5 on 2021-01-21 21:01

from django.db import migrations, models
import quiz.manager


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', quiz.manager.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_superadmin',
            field=models.BooleanField(default=False),
        ),
    ]
