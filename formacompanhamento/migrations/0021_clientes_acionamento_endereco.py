# Generated by Django 5.1.2 on 2025-03-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0020_clientes_acionamento_contato_financeiro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes_acionamento',
            name='endereco',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
