# from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import create_parking_lot, park_the_vehicle, get_parking_lot_status, leave_the_parking_lot

router = DefaultRouter()
urlpatterns = router.urls
urlpatterns.append(path(r'create-parking-lot', create_parking_lot))
urlpatterns.append(path(r'book-or-leave-parking-slot', park_the_vehicle))
urlpatterns.append(path(r'leave-parking-slot', leave_the_parking_lot))
urlpatterns.append(path(r'parking-lot-current-status', get_parking_lot_status))
