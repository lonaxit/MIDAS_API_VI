# Generated by Django 4.0.6 on 2022-07-31 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_mastersavingsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersavingsummary',
            name='transaction_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
