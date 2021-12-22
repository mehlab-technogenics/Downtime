from django.contrib import admin

# Register your models here.
from base.models import Website
from base.models import History
from base.models import Profile
from base.models import webData


admin.site.register(Website)
admin.site.register(History)
admin.site.register(Profile)
admin.site.register(webData)