# Generated by Django 4.2 on 2023-08-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regsys', '0018_alter_registration_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('Подтверждено', 'Aff'), ('Пересекается', 'Int'), ('Очередь', 'Wai'), ('Посещено', 'Vis'), ('Пропущено', 'Mis')], default='Подтверждено', verbose_name='Статус'),
        ),
    ]
