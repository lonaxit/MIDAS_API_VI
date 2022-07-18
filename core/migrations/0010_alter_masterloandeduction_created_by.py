# Generated by Django 4.0.6 on 2022-07-10 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_rename_monthlyloandeduction_masterloandeduction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterloandeduction',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='masterloandeduction', to=settings.AUTH_USER_MODEL),
        ),
    ]
