# Generated by Django 4.1.5 on 2023-02-23 13:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="A spot's name", max_length=100, unique=True)),
                ('latitude', models.DecimalField(decimal_places=6, help_text="This spot's latitude co-ordinate (Lines parallel to the equator, ranging from 90 (North) to -90 (South) degrees", max_digits=8, validators=[django.core.validators.MaxValueValidator(90.0, message='Latitude too high (Max 90)'), django.core.validators.MinValueValidator(-90.0, message='Latitude is too low (Min -90)'), django.core.validators.DecimalValidator(8, 6)])),
                ('longitude', models.DecimalField(decimal_places=6, help_text="This spot's longitude co-ordinate (Lines going from pole to pole, ranging from 180 (East) to -180 (West) degrees", max_digits=9, validators=[django.core.validators.MaxValueValidator(180.0, message='Longitude too high (Max 180)'), django.core.validators.MinValueValidator(-180.0, message='Longitude is too low (Min -180)'), django.core.validators.DecimalValidator(9, 6)])),
                ('average_attendance_int', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='The average whole number of users that come to this spot when it is spot of the day')),
                ('image_pointer', models.PositiveSmallIntegerField(blank=True, default=0, help_text="The ID number of the spot's saved image (range is from 0 to 32767)")),
            ],
            options={
                'verbose_name': 'Spots',
                'verbose_name_plural': 'Spots',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatarId', models.PositiveSmallIntegerField(blank=True, default=0, help_text='The ID number of the users chosen avatar (range is from 0 to 32767)')),
                ('title', models.CharField(help_text='The title chosen by the user to represent them', max_length=100)),
                ('level', models.PositiveSmallIntegerField(blank=True, default=0, help_text='The users current/high score')),
                ('group', models.CharField(choices=[('GR', 'Green'), ('YW', 'Yellow'), ('BL', 'Blue'), ('RD', 'Red')], help_text="The user's group affiliation", max_length=2, null=True)),
                ('user', models.OneToOneField(help_text='Linking this information to the user in auth_User it relates to', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Users Info',
                'verbose_name_plural': 'Additional User Info',
            },
        ),
        migrations.CreateModel(
            name='PreviousSpotAttend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.PositiveSmallIntegerField(default=0, help_text='The number of people that attended this spot')),
                ('spotDay', models.DateField(help_text='The day that this was the spot of the day, represented as the Python datetime.date value', null=True, unique=True)),
                ('sId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exSeed.spot')),
            ],
            options={
                'verbose_name': 'Previous Spot Attendance Record',
                'verbose_name_plural': 'Previous Spot Attendance Record',
            },
        ),
        migrations.CreateModel(
            name='CurrentSpotRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sId', models.ForeignKey(help_text="Today's spot", on_delete=django.db.models.deletion.CASCADE, to='exSeed.spot')),
                ('uId', models.ForeignKey(help_text="This user has attended today's spot", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entries',
                'verbose_name_plural': 'Daily Register',
            },
        ),
    ]
