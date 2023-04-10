# Generated by Django 4.0.6 on 2023-03-01 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0034_rename_ippis_profile_staff_id_remove_profile_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='guarantor_one',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='loanguarantorone', to=settings.AUTH_USER_MODEL),
        ),
    ]
