from django.contrib import admin
from accountstuff.models import UserInfo
from accountstuff.models import Address
from accountstuff.models import CreditCards

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Address)
admin.site.register(CreditCards)