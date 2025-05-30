# Generated by Django 5.1.2 on 2025-04-28 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at'], 'verbose_name': 'Notificação', 'verbose_name_plural': 'Notificações'},
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Visualizado'),
        ),
    ]
