from django.contrib import admin
from MGA.models import User, Event, Organization

admin.site.register(User)
admin.site.register(Organization, Event)
