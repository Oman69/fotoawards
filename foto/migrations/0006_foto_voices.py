# Generated by Django 4.1.3 on 2022-12-23 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foto', '0005_alter_foto_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='voices',
            field=models.IntegerField(default=0),
        ),
    ]