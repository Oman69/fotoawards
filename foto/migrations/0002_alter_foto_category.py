# Generated by Django 4.1.3 on 2022-12-23 16:51

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
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='foto.category', verbose_name='Категория'),
        ),
    ]
