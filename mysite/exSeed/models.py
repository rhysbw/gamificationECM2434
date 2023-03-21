from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

"""
Developer note:
When no field is explicitly defined as the primary key, Django automatically creates an auto-incrementing integer primary key.
This has been used for every model, and thus there are no explicitly stated primary keys
These primary keys can be referenced to with .pk if needed
"""

# Validators
def valid_time(time):
    """Ensures any manual register entries are within valid bounds

    Args:
        time (datetime.time): The time of the register submission

    Raises:
        ValidationError: Time is too early for start time (default is 06:00)
        ValidationError: Time is too late for end time (default is 19:00)

    @author Rowan N
    """
    current_hour = time.hour
    earliest_hour = 9  # This value indicates the earliest hour the user can submit a valid time
    latest_hour = 16  # This value indicates the final hour within which a user can submit a valid time
    if current_hour < earliest_hour:
        raise ValidationError(
            _('%(time)s is not after %(hour)s:00:00'),
            params={'time':time,'hour':earliest_hour},
        )
    elif current_hour > latest_hour:
        raise ValidationError(
            _('%(time)s is not before %(hour)s:59:59'),
            params={'time':time,'hour':latest_hour},
        )


# Create your models here.
class UserInfo(models.Model):
    """This table holds additional data on each user

    Columns:
        user (OneToOneField): This is a link to an existing user in the auth_user table.
            Each user can only have ONE entry in UserInfo (OneToOne relation), and if the user is deleted, the CASCADE option ensures this
            record will also be deleted
        avatarId (ForeignKey): This records what avatar this user has chosen to represent them. This is the avatar ID from the Avatar table.
            Defaults to 1 (the first ID in the avatar table)
        title (CharField): This is the title this user has chosen to represent them on their user page, visable to other users. Can be empty
        totalPoints (PositiveSmallIntegerField): Holds this users total points acquired whilst playing the game
        currentStreak (PositiveSmallIntegerField): Holds this users current points earned back-to-back (daily)
        lastSpotRegister (DateField): Holds the date that this user last registered at a spot. Used when resetting streaks of users who have
            not played yesterday
        hasTakenPledge (BooleanField): Boolean value for if the user has taken the SotD pledge. Means this user cannot access main pages of the
            site if false.
        

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
    )
    totalPoints = models.PositiveSmallIntegerField(
        help_text="The users high score",
        default=0,
        blank=True,
        verbose_name="Points"
    )
    currentStreak = models.PositiveSmallIntegerField(
        help_text="The users current streak",
        default=0,
        blank=True,
        db_index=True,
        verbose_name="Streak"
    )
    lastSpotRegister = models.DateField(
        help_text="The date this user last visited a spot",
        blank=True,
        null=True,
        verbose_name="Last Register Date"
    )
    hasTakenPledge = models.BooleanField(
        help_text="Has the user agreed to the Spot of the Day pledge?",
        default=False,
        verbose_name="Pledged"
    )

    def __str__(self):
        return str(self.user.id) + " " + str(self.user.username) + " [CS=" + \
            str(self.currentStreak) + " TP=" + str(self.totalPoints) + "]"

    class Meta:
        verbose_name_plural = "Additional User Info"
        verbose_name = "Users Info"


class Avatar(models.Model):
    """This table holds all data on the avatars users can choose to represent themselves on the leaderboard and their profile

    Columns:
        imageName (CharField): Holds the link to the image
        avatarTitle (CharField): The name of this avatar, used as a human-readable way to distinguish avatars

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. Fish) (AKA avatarTitle)
    
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
        return self.avatarTitle


class Spot(models.Model):
    """This table holds all data on the spots

    Columns:
        name (CharField): The name of a given spot. This MUST be a unique value
        desc (TextField): A description for the spot, to be found underneath it's picture on the spot page. Can be empty
        latitude (DecimalField): The North-South latitude of this spot. Allows for six decimal places of accuracy. Cannot go over 90 or
            under -90
        longitude (DecimalField): The East-West longitude of this spot. Allows for sex decimal places of accuracy. Cannot go over 180
            or under -180
        average_attendance (PositiveSmallIntegerField): The average attendance of this spot when it is the spot of the day
        imageName (CharField): The link to the image for this spot. Can be empty

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. Duck Pond (ID 1)) (AKA name (ID spotID))
    
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
    average_attendance = models.PositiveSmallIntegerField(  # This field supports a max value of 32767
        help_text="The average whole number of users that come to this spot when it is spot of the day",
        default=0,
        #db_index=True,  # This may be an important value through which to judge spots
    )
    imageName = models.CharField(
        help_text="The link to this spots image",
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.name + " (ID " + str(self.id) + ")"

    class Meta:
        verbose_name = "Spots"
        verbose_name_plural = "Spots"


class UserRegister(models.Model):
    """This table holds which users have attended which spot-instance (record of when a spot is the spot of the day). 

    Columns:
        uId (ForeignKey): The primary key for the user that has attended the spot. A user can attend multiple spots, and as such
            a user can be represented multiple times in the table
        srId (ForeignKey): The primary key of the spot-instance (previousSpotAttend). This is the spot and the day the spot was
            the spot of the day. Since multiple users can register at the same spot, this can be found multiple times in the table
        spotNiceness (PositiveSmallIntegerField): How the user rated the spot when they visited (From one to five stars). This data
            is used to populate the graph mapping spot quality over the day
        registerTime (TimeField): Holds when the user registered their attendance at the spot. This field is automatically populated
            at record inception, and so cannot be spoofed or edited. Used to tell the graph when the users rating applies.
        registerTimeEditable (TimeField): Holds a manually enterable time value, used to test the system and graph.

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. dev attended spot on 1 March at 14:47:09) 
                                                                           (AKA uId.username attended spot on srId.spotDay at registerTime))
    
    Other:
        The meta class defines how information from this table is referred to in the admin screen (named for purpose of clarity)

    @author Rowan N
    """
    uId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="This user has attended today's spot",
    )
    srId = models.ForeignKey(
        'SpotRecord',
        on_delete=models.CASCADE,
        verbose_name="Spot data",
        help_text="Related spot-day instance"
    )

    spotNiceness = models.PositiveSmallIntegerField(
        help_text="The number of stars this user has rated the spot upon attendance (1 to 5)",
        validators=[MaxValueValidator(5, message="Max rating is 5 stars"),
                    MinValueValidator(1, message="Min rating is 1 star")],
    )

    registerTime = models.TimeField(
        auto_now_add=True,
        help_text="The time that the record is created. Note, this field cannot be edited, and is automatically created",
        validators=[valid_time]
    )

    registerTimeEditable = models.TimeField(
        null=True,
        help_text="An admin, alterable time field for the purposes of testing. Can be null upon record creation",
        validators=[valid_time]
    )

    def __str__(self):
        formatted_date = self.srId.spotDay.strftime("%d %B")
        formatted_time = self.registerTime.strftime("%H:%M:%S")
        return str(self.uId.username) + " attended spot on " + str(formatted_date) + " at " + " " + str(formatted_time)

    class Meta:
        verbose_name_plural = "Register"
        verbose_name = "Entries"


class SpotRecord(models.Model):  # SpotRecord
    """This table holds each instance of a spot being the spot of the day 

    Columns:
        sId (ForeignKey): Holds the spot that is the spot of the day. If the spot it's referencing is deleted, this record is also deleted
        attendance (PositiveSmallIntegerField): Records how many individuals have attended this spot-instance. Default is 0
        spotDay (DateField): The actual date this spot is spot of the day. Must be unique (only one spot can be spot of the day)

    Functions:
        __str__(self): Defines how each record in the table is represented (E.g. 26 February - Rock Garden) (AKA spotDay - sId.name)
    
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
        formatted_date = self.spotDay.strftime("%d %B")
        return str(formatted_date) + " - " + self.sId.name

    class Meta:
        verbose_name_plural = "Spot Record"
        verbose_name = "Spot Records"
