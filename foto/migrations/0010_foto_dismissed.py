# Generated by Django 4.1.5 on 2023-01-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0009_delete_userapikey'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='dismissed',
            field=models.BooleanField(default=False, verbose_name='Отклонено'),
        ),
    ]