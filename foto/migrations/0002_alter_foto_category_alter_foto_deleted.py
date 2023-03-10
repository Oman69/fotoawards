# Generated by Django 4.1.5 on 2023-02-09 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='category',
            field=models.ForeignKey(default=4, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='foto.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='На удалении'),
        ),
    ]
