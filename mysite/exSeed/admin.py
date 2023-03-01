from django.contrib import admin
from .models import UserInfo, Spot, SpotRegister, PreviousSpotAttend, Avatar

# Register your models here.
# These lines allow for the viewing and editing of these custom models in the admin page
admin.site.register(UserInfo)
admin.site.register(Spot)
admin.site.register(SpotRegister)
admin.site.register(PreviousSpotAttend)
admin.site.register(Avatar)
