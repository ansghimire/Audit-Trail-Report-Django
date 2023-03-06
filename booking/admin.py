from django.contrib import admin

# Register your models here.
from .models import Booking,BookingAuditTrail

admin.site.register(Booking)
admin.site.register(BookingAuditTrail)