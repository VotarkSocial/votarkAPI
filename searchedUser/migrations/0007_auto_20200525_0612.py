# Generated by Django 3.0.4 on 2020-05-25 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votarkUser', '0013_auto_20200511_2141'),
        ('searchedUser', '0006_auto_20200525_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searcheduser',
            name='searchedUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searched', to='votarkUser.VotarkUser'),
        ),
        migrations.AlterField(
            model_name='searcheduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userSearches', to='votarkUser.VotarkUser'),
        ),
    ]