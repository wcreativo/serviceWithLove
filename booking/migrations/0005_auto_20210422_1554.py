# Generated by Django 3.1.8 on 2021-04-22 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_charge_chargehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datetimedisabler',
            name='to_date',
        ),
        migrations.AlterField(
            model_name='datetimedisabler',
            name='from_date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='datetimedisabler',
            name='from_time',
            field=models.TimeField(blank=True, null=True, verbose_name='From this time'),
        ),
        migrations.AlterField(
            model_name='datetimedisabler',
            name='to_time',
            field=models.TimeField(blank=True, null=True, verbose_name='To this time'),
        ),
    ]
