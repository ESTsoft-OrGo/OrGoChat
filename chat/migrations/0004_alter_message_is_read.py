# Generated by Django 4.2.4 on 2023-09-21 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_is_read_room_joinuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
