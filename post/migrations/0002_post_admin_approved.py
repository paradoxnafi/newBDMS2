# Generated by Django 4.0.4 on 2022-05-04 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='admin_approved',
            field=models.BooleanField(default=False),
        ),
    ]
