# Generated by Django 3.2.4 on 2022-10-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0063_auto_20221014_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='mutuellesante',
            name='date_appel',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='mutuellesante',
            name='date_rappel',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='mutuellesante',
            name='heure',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
