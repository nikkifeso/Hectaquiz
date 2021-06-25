# Generated by Django 3.1.2 on 2021-06-20 20:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
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
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superadmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='quiztaker',
            name='date_completed',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='usersanswer',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.answer'),
        ),
    ]
