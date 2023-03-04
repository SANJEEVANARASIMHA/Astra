from django.contrib import admin

# Register your models here.
from alert.models import Alert

admin.site.register(Alert)