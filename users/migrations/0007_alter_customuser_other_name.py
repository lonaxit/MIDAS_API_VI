# Generated by Django 4.0.6 on 2023-02-21 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_avatar_customuser_dob_customuser_dofa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='other_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
