# Generated by Django 5.2.3 on 2025-07-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_publishedsciwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Наименование работы')),
                ('mark', models.TextField(max_length=100, verbose_name='Отметка о выполнении')),
            ],
        ),
    ]
