# Generated by Django 3.0.4 on 2020-05-12 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200512_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='isMonetizedMonthly',
        ),
        migrations.RemoveField(
            model_name='post',
            name='isMonetizedWeekly',
        ),
        migrations.RemoveField(
            model_name='post',
            name='isMonetizedYearly',
        ),
    ]
