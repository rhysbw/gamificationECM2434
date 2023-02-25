from django.contrib import admin
from .models import UserInfo, Spot, SpotRegister, PreviousSpotAttend, Avatar

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Spot)
admin.site.register(SpotRegister)
admin.site.register(PreviousSpotAttend)
admin.site.register(Avatar)
