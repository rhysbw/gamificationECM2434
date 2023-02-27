from django.apps import AppConfig
import datetime
import random

class ExseedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exSeed'

    def ready(self):
        from exSeed.models import Spot, PreviousSpotAttend
        today = datetime.date.today()

        spots = PreviousSpotAttend.objects.filter(spotDay=today)
        yesterday = today - datetime.timedelta(days=1)

        if len(spots) == 0:
            while True:
                #pick a random spot
                spot = random.choice(Spot.objects.all())
                # check if that is the same as yesterday and if so get a new one
                try:
                    if spot.id != PreviousSpotAttend.objects.filter(spotDay=yesterday)[0].sId:
                        break
                except IndexError:
                    break
            PreviousSpotAttend(sId=spot, attendance=0, spotDay=today).save()
            print("spot of the day assigned")
        else:
            print("spot was already assigned")

