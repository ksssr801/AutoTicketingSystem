from .models import ParkingDetails, SlotDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# To create parking lot
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def create_parking_lot(request):
    msg = ''
    slot_size = int(request.GET.get('parking_lot_size', 0))
    if slot_size:
        msg = 'Created a parking lot with %s slot(s).' % slot_size
        SlotDetails.objects.all().delete()
        for i in range(1,slot_size+1):
            new_obj = SlotDetails(slot=i)
            new_obj.save()
        return Response({'msg': msg, 'parking_lot_size': slot_size}, template_name='create-parking-lot-template.html')
    else:
        msg = 'Slot size should be greater than 0.'
        return Response({'msg': msg}, template_name='create-parking-lot-template.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def park_the_vehicle(request):
    reg_num = str(request.GET.get('reg_num', ''))
    color = str(request.GET.get('color', ''))
    if reg_num and color:
        count = ParkingDetails.objects.filter(registration_no=reg_num, color=color).count()
        if not count:
            all_empty_slots = [slot_obj.get('slot', None) for slot_obj in SlotDetails.objects.values().filter(is_booked=False)]
            if len(all_empty_slots):
                nearest_empty_slot = min(all_empty_slots)
                new_obj = ParkingDetails(registration_no=reg_num, color=color, allocated_slot=SlotDetails.objects.get(slot=nearest_empty_slot))
                new_obj.save()
                SlotDetails.objects.filter(slot=nearest_empty_slot).update(is_booked=True)
                return render(request, 'booking-parking-lot-template.html', {'allocated_slot_num': nearest_empty_slot, 'reg_num': reg_num, 'color': color})
            else:
                return render(request, 'booking-parking-lot-template.html', {'full_status': 'Sorry, Parking Slot is full.', 'reg_num': reg_num, 'color': color})
        else:
            status = 'Car with registration num: %s and color: %s is already present.' % (reg_num, color)
            return render(request, 'booking-parking-lot-template.html', {'status1': status, 'reg_num': reg_num, 'color': color})
    else:
        return render(request, 'booking-parking-lot-template.html', {'status2': 'All fields are mandatory under booking !', 'reg_num': reg_num, 'color': color})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def leave_the_parking_lot(request):
    slot_to_leave = request.GET.get('slot_num', 0)
    msg = ''
    if slot_to_leave:
        ret_data = SlotDetails.objects.filter(slot=slot_to_leave).values()
        if len(ret_data):
            if ret_data[0].get('is_booked'):
                res = SlotDetails.objects.filter(slot=slot_to_leave).update(is_booked=False)
                if res:
                    ParkingDetails.objects.filter(allocated_slot=SlotDetails.objects.get(slot=slot_to_leave)).delete()
                    msg = 'Slot number %s is free.' % slot_to_leave
                else:
                    msg = 'Particular Slot %s is not present in parking lot.'
            else:
                msg = 'Particular Slot %s is already free.' % slot_to_leave
        else:
            msg = 'Particular Slot %s is not present in parking lot.' % slot_to_leave
    return render(request, 'booking-parking-lot-template.html', {'msg': msg})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def get_parking_lot_status(request):
    color = str(request.GET.get('color',''))
    reg_num = str(request.GET.get('reg_num',''))
    parking_slot_size = SlotDetails.objects.values_list(flat=True).count()
    empty_slots = SlotDetails.objects.values_list(flat=True).filter(is_booked=False)
    empty_slots = str(list(empty_slots))[1:-1]
    if not empty_slots:
        empty_slots = 'All Full.'
    if color:
        parking_dataset = ParkingDetails.objects.filter(color__contains=color).values()
    elif reg_num:
        parking_dataset = ParkingDetails.objects.filter(registration_no__contains=reg_num).values()
    else:
        parking_dataset = ParkingDetails.objects.values()
    
    for obj in parking_dataset:
        obj.update({'ticket_id':'SlotTkt'+str(obj.get('ticket_id'))})
    final_dict = {'parking_lot_status': parking_dataset}
    return render(request, 'parking-lot-status-template.html', {'final_dict': final_dict, 'color': color, 'reg_num': reg_num, 'empty_slots': empty_slots, 'parking_slot_size': parking_slot_size})
