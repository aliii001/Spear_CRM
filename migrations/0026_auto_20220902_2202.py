# Generated by Django 3.2.4 on 2022-09-02 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0025_bilan_user_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_admin',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bilan',
            name='user_admin',
            field=models.IntegerField(default=2, null=True),
        ),
    ]
