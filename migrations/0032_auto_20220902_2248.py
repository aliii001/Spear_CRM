# Generated by Django 3.2.4 on 2022-09-02 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0031_event_user_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='nom_agent',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='prenom_agent',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='username_agent',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
