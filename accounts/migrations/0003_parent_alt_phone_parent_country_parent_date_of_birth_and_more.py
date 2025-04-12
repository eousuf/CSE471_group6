# Generated by Django 5.2 on 2025-04-12 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_parent_name_alter_parent_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='alt_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='parent',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='parent',
            name='emergency_relation',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='parent',
            name='home_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='parent',
            name='previous_employers',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='profession',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='parent',
            name='state',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='work_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='parent',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='parent',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
