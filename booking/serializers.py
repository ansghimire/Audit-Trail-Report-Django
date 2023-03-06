from .models import Booking, BookingAuditTrail
from rest_framework import serializers


class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','booking_number','booking_name','invoice_no','title','contact_no']
        read_only_fields = ['id']


class BookingAuditTrailSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingAuditTrail
        fields = '__all__'