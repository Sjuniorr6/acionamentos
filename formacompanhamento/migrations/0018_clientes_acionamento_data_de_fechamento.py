# Generated by Django 5.1.2 on 2025-03-19 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0017_clientes_acionamento_atividade_principal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes_acionamento',
            name='data_de_fechamento',
            field=models.DateField(blank=True, help_text='Informe a data de fechamento, se aplicável.', null=True, verbose_name='Data de Fechamento'),
        ),
    ]
