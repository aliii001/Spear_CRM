# Generated by Django 3.2.6 on 2022-01-04 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0006_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='color',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
