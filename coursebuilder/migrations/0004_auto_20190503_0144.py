# Generated by Django 2.1.2 on 2019-05-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursebuilder', '0003_delete_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulesection',
            name='order',
            field=models.IntegerField(),
        ),
    ]
