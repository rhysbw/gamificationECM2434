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
    avatarId = models.ForeignKey(
        'Avatar',
        on_delete=models.CASCADE,
        help_text="User's chosen avatar",
        default=1,
    )
    title = models.CharField(
        help_text="The title chosen by the user to represent them",
        max_length=100,
        blank=True,
        # ! Don't know how we are dealing with this. Is this the actual title, or just a reference to a title
    )
    totalPoints = models.PositiveSmallIntegerField(
        help_text="The users high score",
        default=0,
        blank=True,
    )
    currentStreak = models.PositiveSmallIntegerField(
        help_text="The users current streak",
        default=0,
        blank=True,
        db_index=True,
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
        blank=True,
    )

    def __str__(self):
        return str(self.user.id) + " " + str(self.user.username) + " [CS=" + \
            str(self.currentStreak) + " TP=" + str(self.totalPoints) + "]"

    class Meta:
        verbose_name_plural = "Additional User Info"
        verbose_name = "Users Info"


class Avatar(models.Model):
    imageName = models.CharField(
        help_text="The png name of the avatar image",
        max_length=100,
    )
    avatarTitle = models.CharField(
        help_text="The name found under the avatar in the selection menu",
        max_length=100,
    )

    def __str__(self):
        return self.imageName


class Spot(models.Model):
    name = models.CharField(
        help_text="A spot's name",
        unique=True,  # Unique implies db_index = True
        max_length=100,
    )
    desc = models.TextField(
        help_text="A description of the spot, to appear when a user sees the spot",
        max_length=500,
        null=True,  # Allows a spot to be created without needing a description at moment of creation
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
        #db_index=True,  # This may be an important value through which to judge spots
    )
    imageName = models.CharField(
        help_text="The name of the png file that holds this spots image",
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.name + " (ID " + str(self.id) + ")"

    class Meta:
        verbose_name = "Spots"
        verbose_name_plural = "Spots"


class SpotRegister(models.Model):
    uId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="This user has attended today's spot",
    )
    psaId = models.ForeignKey(
        'PreviousSpotAttend',
        on_delete=models.CASCADE,
        verbose_name="Spot data",
        help_text="Related spot-day instance"
    )

    def __str__(self):
        return str(self.uId.username) + " attended the spot on " + str(self.psaId.spotDay)

    class Meta:
        verbose_name_plural = "Register"
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
        db_index=True,  # Orders entries by date submitted
    )

    def __str__(self):
        return str(self.spotDay) + " " + self.sId.name

    class Meta:
        verbose_name_plural = "Spot Record"
        verbose_name = "Spot Records"
