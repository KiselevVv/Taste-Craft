# Generated by Django 3.2.18 on 2023-04-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=24, verbose_name='Единица измерения'),
        ),
    ]
