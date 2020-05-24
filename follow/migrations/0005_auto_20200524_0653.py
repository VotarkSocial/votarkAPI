# Generated by Django 3.0.4 on 2020-05-24 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('versus', '0003_auto_20200520_2352'),
        ('votarkUser', '0013_auto_20200511_2141'),
        ('follow', '0004_auto_20200520_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='votarkUser.VotarkUser'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='onVersus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='versus.Versus'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userfollows', to='votarkUser.VotarkUser'),
        ),
    ]