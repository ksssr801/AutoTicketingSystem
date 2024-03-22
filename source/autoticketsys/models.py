from __future__ import unicode_literals
from django.db import models
from django.db.models.deletion import CASCADE

class SlotDetails(models.Model):
    slot = models.IntegerField(primary_key=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_slot_details'

class ParkingDetails(models.Model):
    ticket_id = models.AutoField(primary_key=True, db_column='ticket_id')
    registration_no = models.CharField(max_length=500, null=False)
    color = models.CharField(max_length=500, null=False)
    allocated_slot = models.ForeignKey(SlotDetails, db_column='slot', related_name='parking_slot_id_mapping',on_delete=CASCADE)

    class Meta:
        db_table = 'tbl_parking_details'

