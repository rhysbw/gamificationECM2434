from django.apps import AppConfig, apps
import datetime
import random


class ExseedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exSeed'


    def ready(self):
        """Function that is run when the server boots up to assign a spot of the day if one hasn't been assigned
        yet

        Returns:
            Null

        @author: Benjamin
        """
        '''
        # Imports the models within the function as this function only runs when it is ready
        from .models import SpotRecord, Spot

        # Assigns variables for the date today and yesterday and checks to see if there are any
        # spots that are assigned for today
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        spots = SpotRecord.objects.filter(spotDay=today)

        # Condition checks if there are any spots assigned for today otherwise no code will run
        if len(spots) == 0:
            # Loop will repeat until a random spot is selected that is not the same spot as yesterday
            while True:
                # pick a random spot
                spot = random.choice(Spot.objects.all())
                # check if that is the same as yesterday and if so repeat the loop to find a new one
                try:
                    if spot.id != SpotRecord.objects.filter(spotDay=yesterday)[0].sId:
                        break
                except IndexError:
                       break
            # Saves the spot in the pervious spot attend database
            SpotRecord(sId=spot, attendance=0, spotDay=today).save()
'''