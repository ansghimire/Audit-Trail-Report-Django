from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import action
from .models import Booking, BookingAuditTrail
from .serializers import BookingSerializers, BookingAuditTrailSerializers
from rest_framework.response import Response


# if updation occur in Booking model this will trigger
def create_audit_trail_for_updation_of_booking(self, previous_value, new_value):
        booking_id = previous_value.pop('id','')
        new_value.pop('id','')
        previous_value.pop('_state', '')


        ### Helps to get only the updated values
        changes_value = { prev : new_value[prev] for prev in previous_value if previous_value[prev] != new_value[prev]}
        
        for key,value in changes_value.items():
            
             previous_data = previous_value[key]

             BookingAuditTrail.objects.create(booking_id=booking_id,
                                                 field_name = key,
                                                 previous_data = previous_data,
                                                 new_data = value
                                                 )
             


# Create your views here.
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers

    def perform_create(self, serializer):
        data = serializer.save()
        if self.action == 'create':
            
            for key, value in serializer.data.items():
                BookingAuditTrail.objects.create(booking_id=data.id,
                                                 field_name = key,
                                                 new_data = value
                                                 )
                               
                
    def perform_update(self, serializer):
        booking_number = self.request.data.get('booking_number')
        previous_value = Booking.objects.get(booking_number=booking_number)
        try:
            super().perform_update(serializer)
            # print('previous data', previous_value.__dict__)
            # print('new data',serializer.data)
            previous_value = previous_value.__dict__
            new_data = serializer.data
            create_audit_trail_for_updation_of_booking(self, previous_value, new_data)

        except:
            return Response("Something went wrong while updating")
        
    
    def perform_destroy(self, instance):
         deleted_instance = instance.__dict__
         deleted_instance.pop('_state', '')
         for key, value in deleted_instance.items():
                BookingAuditTrail.objects.create(booking_id=instance.id,
                                                 field_name = key,
                                                 previous_data = value
                                                 )

         return super().perform_destroy(instance)


    @action(detail=True, url_path="audit-trail")
    def booking_audit_trail(self, *args, **kwargs):
         booking_obj = self.get_object()
         
         booking_audit_trail = BookingAuditTrail.objects.filter(booking_id=booking_obj.id)
         ser = BookingAuditTrailSerializers(data=booking_audit_trail, many=True)
         return Response(ser.data)


    









    