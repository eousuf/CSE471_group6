# Generated by Django 5.2 on 2025-04-17 20:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='daycare',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daycares', to=settings.AUTH_USER_MODEL),
        ),
    ]
