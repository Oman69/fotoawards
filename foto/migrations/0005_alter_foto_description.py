# Generated by Django 4.1.3 on 2022-12-23 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0004_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание'),
        ),
    ]
