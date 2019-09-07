from django.contrib import admin

# Register your models here.
from logic.models import Role, Ability, Buff

admin.site.register(Role)
admin.site.register(Ability)
admin.site.register(Buff)