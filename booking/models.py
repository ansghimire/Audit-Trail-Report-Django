from django.db import models

# Create your models here.
class Booking(models.Model):
    booking_number = models.IntegerField()
    booking_name = models.CharField(max_length=255)
    invoice_no = models.IntegerField()
    title = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.booking_name
    
    def save(self, *args, **kwargs):   
        super(Booking, self).save(*args, **kwargs)
    

class BookingAuditTrail(models.Model):
    booking_id = models.IntegerField()
    field_name = models.CharField(max_length=100)
    previous_data = models.CharField(max_length=100)
    new_data = models.CharField(max_length=100)
    # done_by
    done_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.booking_id}  --> fieldName-{self.field_name} --> prev-{self.previous_data} --> newdata-{self.new_data}'
    

    

