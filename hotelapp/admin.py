from django.contrib import admin
from .models import Hotel, Room, Reservation


admin.site.register(Hotel)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "hotel")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "start", "end")
