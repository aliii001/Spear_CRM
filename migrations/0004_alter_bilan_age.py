# Generated by Django 3.2.6 on 2022-01-02 01:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0003_auto_20220102_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilan',
            name='age',
            field=models.IntegerField(default=1, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
