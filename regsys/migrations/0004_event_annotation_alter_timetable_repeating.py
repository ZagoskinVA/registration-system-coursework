# Generated by Django 4.2 on 2023-05-03 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regsys', '0003_alter_event_options_alter_guest_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='annotation',
            field=models.CharField(default='какая-то аннотация для события', max_length=1000, verbose_name='Аннотация'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='repeating',
            field=models.BooleanField(verbose_name='Повтор?'),
        ),
    ]
