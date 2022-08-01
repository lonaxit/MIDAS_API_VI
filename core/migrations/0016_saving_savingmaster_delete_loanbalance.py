# Generated by Django 4.0.6 on 2022-07-31 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0015_loanbalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('debit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_code', models.BigIntegerField()),
                ('transaction_date', models.DateField()),
                ('narration', models.CharField(max_length=350)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='savinguser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ippis_number', models.PositiveBigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_code', models.BigIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('transaction_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='savingmasteruser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Loanbalance',
        ),
    ]
