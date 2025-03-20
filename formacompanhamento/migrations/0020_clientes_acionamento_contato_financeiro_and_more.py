# Generated by Django 5.1.2 on 2025-03-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0019_clientes_acionamento_contrato_pdf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes_acionamento',
            name='contato_financeiro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes_acionamento',
            name='contato_legal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes_acionamento',
            name='contato_operacional',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes_acionamento',
            name='representante_financeiro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes_acionamento',
            name='representante_operacional',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
