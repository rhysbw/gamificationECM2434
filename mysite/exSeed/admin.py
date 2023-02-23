from django.contrib import admin
from .models import UserInfo, Spot, CurrentSpotRegister,PreviousSpotAttend

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Spot)
admin.site.register(CurrentSpotRegister)
admin.site.register(PreviousSpotAttend)
