# Generated by Django 4.1.6 on 2023-02-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exSeed', '0002_avatar_spotregister_alter_previousspotattend_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='currentStreak',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, default=0, help_text='The users current streak'),
        ),
    ]