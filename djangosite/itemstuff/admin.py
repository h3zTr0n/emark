from __future__ import absolute_import

from django.contrib import admin
from itemstuff.models import Item, Review
from .models import Motor
from .models import Event
from .models import Electronics
from .models import BoutiquesFashion

# Register your models here.
class EventModelAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by", "advertisers_name"]

admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Motor)
admin.site.register(Event, EventModelAdmin)
admin.site.register(Electronics)
admin.site.register(BoutiquesFashion)
