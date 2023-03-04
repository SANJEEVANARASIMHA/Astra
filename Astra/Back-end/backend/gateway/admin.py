from django.contrib import admin

# Register your models here.
from gateway.models import MasterGateway, SlaveGateway

admin.site.register(MasterGateway)
admin.site.register(SlaveGateway)
