# Generated by Django 3.2.4 on 2022-09-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0029_alter_suivi_user_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='user_admin',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
