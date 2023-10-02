# Generated by Django 4.2.4 on 2023-09-30 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='study',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='study_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.groupchat'),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupchat',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupchat',
            name='study',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='study.study'),
        ),
    ]