# Generated by Django 3.2.6 on 2022-01-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0017_alter_stockage_loisir'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='user_id',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
