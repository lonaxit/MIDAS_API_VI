# Generated by Django 4.0.6 on 2022-07-31 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_masterloandeductionsummary_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingmaster',
            name='narration',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
