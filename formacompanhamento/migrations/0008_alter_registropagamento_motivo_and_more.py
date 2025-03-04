# Generated by Django 5.1.6 on 2025-02-13 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacompanhamento', '0007_alter_registropagamento_motivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registropagamento',
            name='motivo',
            field=models.CharField(blank=True, choices=[('Antenista', 'Antenista'), ('Pronta Resposta Armado', 'Pronta Resposta Armado'), ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registropagamento',
            name='motivo1',
            field=models.CharField(blank=True, choices=[('Antenista', 'Antenista'), ('Pronta Resposta Armado', 'Pronta Resposta Armado'), ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registropagamento',
            name='motivo2',
            field=models.CharField(blank=True, choices=[('Antenista', 'Antenista'), ('Pronta Resposta Armado', 'Pronta Resposta Armado'), ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registropagamento',
            name='motivo3',
            field=models.CharField(blank=True, choices=[('Antenista', 'Antenista'), ('Pronta Resposta Armado', 'Pronta Resposta Armado'), ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado')], max_length=50, null=True),
        ),
    ]
