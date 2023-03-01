from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator

"""
Developer note:
When no field is explicitly defined as the primary key, Django automatically creates an auto-incrementing integer primary key.
This has been used for every model, and thus there are no explicitly stated primary keys
These primary keys can be referenced to with .pk if needed
"""

# Create your models here.
class UserInfo(models.Model):
    """This table holds additional data on each user

    Columns:
        user (OneToOneField): This is a link to an existing user in the auth_user table.
            Each user can only have ONE entry in UserInfo (OneToOne relation), and if the user is deleted, the CASCADE option ensures this
            record will also be deleted
        avatarId (ForeignKey): This records what avatar this user has chosen to represent them. This is the avatar ID from the Avatar table
            It defaults to 1 (the first ID in the avatar table)
        title (CharField): This is the title this user has chosen to represent them on their user page, visable to other users. Can be empty
        totalPoints (PositiveSmallIntegerField): Holds this users total points acquired whilst playing the game
        currentStreak (PositiveSmallIntegerField): Holds this users current points earned back-to-back (daily)
        group (CharField): Holds the group this user is affiliated with. Can be empty

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. 7 dev [CS=1 TP=1]) (AKA ID Username [currentStreak totalPoints])
    
    Other:
        The meta class defines how information from this table is referred to in the admin screen (named for purpose of clarity)

    @author Rowan N
    """
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
    """This table holds all data on the avatars users can choose to represent themselves

    Columns:
        imageName (CharField): Holds the name of the .png file this image is saved as
        avatarTitle (CharField): The name of this avatar, used as a human-readable way to distinguish avatars

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. avatar1.png) (AKA imageName)
    
    Other:

    @author Rowan N
    """
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
    """This table holds all data on the spots

    Columns:
        name (CharField): The name of a given spot. This MUST be a unique value
        desc (TextField): A description for the spot, to be found underneath it's picture on the spot page. Can be empty
        latitude (DecimalField): The North-South latitude of this spot. Allows for six decimal places of accuracy. Cannot go over 90 or
            under -90
        longitude (DecimalField): The East-West longitude of this spot. Allows for sex decimal places of accuracy. Cannot go over 180
            or under -180
        average_attendance_int (PositiveSmallIntegerField): The average attendance of this spot when it is the spot of the day
        imageName (CharField): The .png name of the file that holds the image for this spot. Can be empty

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. Duck Pond (ID 1)) (AKA name (spotID))
    
    Other:
        The meta class defines how information from this table is referred to in the admin screen (named for purpose of clarity)

    @author Rowan N
    """
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
    """This table holds which users have attended which spot-instance (record of when a spot is the spot of the day). 

    Columns:
        uId (ForeignKey): The primary key for the user that has attended the spot. A user can attend multiple spots, and as such
            a user can be represented multiple times in the table
        psaId (ForeignKey): The primary key of the spot-instance (previousSpotAttend). This is the spot and the day the spot was
            the spot of the day. Since multiple users can register at the same spot, this can be found multiple times in the table

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. dev attended the spot on 2023-03-01) 
                                                                           (AKA uId.username attended the spot on psaId.spotDay))
    
    Other:
        The meta class defines how information from this table is referred to in the admin screen (named for purpose of clarity)

    @author Rowan N
    """
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
    """This table holds each instance of a spot being the spot of the day 

    Columns:
        name (_type_): _description_
        sId (ForeignKey): Holds the spot that is the spot of the day. If the spot it's referencing is deleted, this record is also deleted
        attendance (PositiveSmallIntegerField): Records how many individuals have attended this spot-instance. Default is 0
        spotDay (DateField): The actual date this spot is spot of the day. Must be unique (only one spot can be spot of the day)

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. 2023-02-26 Rock Garden) (AKA spotDay sId.name)
    
    Other:
        The meta class defines how information from this table is referred to in the admin screen (named for purpose of clarity)

    @author Rowan N
    """
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
