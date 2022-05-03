# Generated by Django 4.0.4 on 2022-05-02 14:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='read_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
