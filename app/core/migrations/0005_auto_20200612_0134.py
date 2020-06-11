# Generated by Django 2.1.15 on 2020-06-12 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200611_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='core.Recipe'),
        ),
    ]
