# Generated by Django 4.0.1 on 2022-03-06 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0002_alter_receitas_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receitas',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
