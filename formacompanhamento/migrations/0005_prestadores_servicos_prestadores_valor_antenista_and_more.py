# Generated by Django 5.1.6 on 2025-02-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0004_registropagamento_motivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestadores',
            name='servicos',
            field=models.CharField(blank=True, choices=[('Antenista', 'Antenista'), ('Ponta Resposta Armado', 'Ponta Resposta Armado'), ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado'), ('Todos os serviços', ' Todos os servicos')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='prestadores',
            name='valor_antenista',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='prestadores',
            name='valor_prontaresposta_armado',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='prestadores',
            name='valor_prontaresposta_desarmado',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
