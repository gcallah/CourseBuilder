# Generated by Django 2.1.2 on 2019-10-25 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursebuilder', '0006_auto_20191018_1959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extras',
            options={'verbose_name_plural': 'Quizes'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'Quizes'},
        ),
    ]
