# Generated by Django 5.1.2 on 2025-03-31 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0026_registropagamento_total_agentes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registropagamento',
            name='total_agentes',
        ),
    ]
