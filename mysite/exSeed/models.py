from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator


# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(
        User,
        help_text="Linking this information to the user in auth_User it relates to",
        on_delete=models.CASCADE,
    )
    avatarId = models.PositiveSmallIntegerField(
        help_text="The ID number of the users chosen avatar (range is from 0 to 32767)",
        default=0,  # All users initially have the same default pfp
        blank=True,
    )
    title = models.CharField(
        help_text="The title chosen by the user to represent them",
        max_length=100,
        # ! Don't know how we are dealing with this. Is this the actual title, or just a reference to a title
    )
    level = models.PositiveSmallIntegerField(
        help_text="The users current/high score",  # Is this the current score or highest score?
        default=0,
        blank=True,
    )
    # Group options
    GREEN = "GR"
    YELLOW = "YW"
    BLUE = "BL"
    RED = "RD"
    GROUP_CHOICES = [(GREEN, "Green"), (YELLOW, "Yellow"), (BLUE, "Blue"), (RED, "Red")]
    #
    group = models.CharField(
        help_text="The user's group affiliation",
        max_length=2,
        choices=GROUP_CHOICES,
        null=True,
    )

    def __str__(self):
        return str(self.user.id) + " " + str(self.user.username)

    class Meta:
        verbose_name_plural = "Additional User Info"
        verbose_name = "Users Info"


class Spot(models.Model):
    name = models.CharField(
        help_text="A spot's name",
        unique=True,  # Unique implies db_index = True
        max_length=100,
    )
    latitude = models.DecimalField(
        help_text="This spot's latitude co-ordinate (Lines parallel to the equator, ranging from 90 (North) to -90 ("
                  "South) degrees",
        max_digits=8,
        decimal_places=6,
        validators=[MaxValueValidator(90.0, message="Latitude too high (Max 90)"),
                    MinValueValidator(-90.0, message="Latitude is too low (Min -90)"),
                    DecimalValidator(8, 6)],
    )
    longitude = models.DecimalField(
        help_text="This spot's longitude co-ordinate (Lines going from pole to pole, ranging from 180 (East) to -180 "
                  "(West) degrees",
        max_digits=9,
        decimal_places=6,
        validators=[MaxValueValidator(180.0, message="Longitude too high (Max 180)"),
                    MinValueValidator(-180.0, message="Longitude is too low (Min -180)"),
                    DecimalValidator(9, 6)],
    )
    average_attendance_int = models.PositiveSmallIntegerField(  # This field supports a max value of 32767
        help_text="The average whole number of users that come to this spot when it is spot of the day",
        default=0,
        db_index=True,  # This may be an important value through which to judge spots
    )
    image_pointer = models.PositiveSmallIntegerField(
        help_text="The ID number of the spot's saved image (range is from 0 to 32767)",
        default=0,  # default value when spot is created
        blank=True,
    )

    def __str__(self):
        return self.name + " (ID " + str(self.id) + ")"

    class Meta:
        verbose_name = "Spots"
        verbose_name_plural = "Spots"


class CurrentSpotRegister(models.Model):
    uId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="This user has attended today's spot",
    )
    sId = models.ForeignKey(
        'Spot',
        on_delete=models.CASCADE,
        help_text="Today's spot",
    )

    def __str__(self):
        return str(self.uId)

    class Meta:
        verbose_name_plural = "Daily Register"
        verbose_name = "Entries"


class PreviousSpotAttend(models.Model):
    sId = models.ForeignKey(
        'Spot',
        on_delete=models.CASCADE,
    )
    attendance = models.PositiveSmallIntegerField(
        help_text="The number of people that attended this spot",
        default=0,
    )
    spotDay = models.DateField(
        help_text="The day that this was the spot of the day, represented as the Python datetime.date value",
        unique=True,  # This implies db_index = True
        null=True,
    )

    class Meta:
        verbose_name_plural = "Previous Spot Attendance Record"
        verbose_name = "Previous Spot Attendance Record"
