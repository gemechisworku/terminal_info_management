# Generated by Django 5.0.3 on 2024-07-12 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0002_terminal_delete_atmterminal'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='type',
            field=models.CharField(default='Hitachi CRM', max_length=20),
        ),
    ]
