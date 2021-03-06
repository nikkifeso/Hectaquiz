# Generated by Django 3.1.5 on 2021-01-24 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210122_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='date_completed',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='usersanswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.answer'),
        ),
    ]
