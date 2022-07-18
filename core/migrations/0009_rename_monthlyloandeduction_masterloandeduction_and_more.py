# Generated by Django 4.0.6 on 2022-07-10 18:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_remove_monthlyloandeductionsummary_entry_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MonthlyLoanDeduction',
            new_name='MasterLoanDeduction',
        ),
        migrations.RenameModel(
            old_name='MonthlyLoanDeductionSummary',
            new_name='MasterLoanDeductionSummary',
        ),
    ]
