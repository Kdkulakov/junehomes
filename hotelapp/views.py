from django.utils import timezone
from django.db.models import F, Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from itertools import chain
from .models import Hotel, Reservation, Room
TODAY = timezone.now().date()


def index(request):
    return render(request, 'index.html')


def like_hotel_view(request, hotel_id):
    if hotel_id:
        hotel = Hotel.objects.filter(pk=hotel_id).update(likes=F('likes') + 1)
        if hotel:
            return HttpResponse('success', 200)
        else:
            return HttpResponse('Not find hotel with this id', 404)


def dislike_hotel_view(request, hotel_id):
    if hotel_id:
        hotel = Hotel.objects.filter(pk=hotel_id).update(dislikes=F('dislikes') + 1)
        if hotel:
            return HttpResponse('success', 200)
        else:
            return HttpResponse('Not find hotel with this id', 404)


def get_all_guests_in_hotel(request, hotel_name):
    hotel = get_object_or_404(Hotel, title=hotel_name)

    reservations = Reservation.objects.filter(room__hotel=hotel, start__lte=TODAY, end__gte=TODAY).values('user__username')
    if hotel:
        return JsonResponse({'guests': list(reservations)})
    return HttpResponse(404)


def get_rooms_list_with_sold_out_sign(request, move_in, move_out):
    move_in_date = timezone.datetime.strptime(move_in, '%Y-%m-%d')
    move_out_date = timezone.datetime.strptime(move_out, '%Y-%m-%d')
    if move_in and move_out:
        ht = Hotel.objects.all()
        soldout_list = ht.annotate(room_s=Count('rooms__reservations')).annotate(
            sold_out=F('room_s')).filter(
            sold_out=True
        ).values(
            'title',
            'rooms__title',
            'rooms__reservations__start',
            'rooms__reservations__end',
            'sold_out'
        )
        free_rooms = ht.annotate(
            room_s=F('rooms__title'), reserv=Count('rooms__reservations')).filter(
            reserv=False,
        ).values(
            'title',
            'rooms__title',
            'room_s',
            'reserv'
        )
        rooms_chain = list(chain(free_rooms, soldout_list))
        return render(request, 'sold_out_list.html', context={'objects': rooms_chain})
    else:
        return JsonResponse({'sold_out_rooms': ''})


def get_list_of_hotels_with_only_one_free_room(request):
    """Не смог я тут выстроить правильный зпрос для получения
    разницы в один объект. :(
    Не гугл не поиск в доках не помог. Буду изучать данный момент.
    Сдаю как есть.
    """
    qs = Hotel.objects.all()
    hotels_list = qs.\
        filter(
            rooms__reservations__start=TODAY,
            rooms__reservations__end=TODAY,
        )\
        .annotate(
            reservations_s=Count('rooms__reservations'),
            room_in_hotel=Count('rooms'),
        ) \
            .filter(
            reservations_s__gt=(F('room_in_hotel') - 1)
        ) \
            .values_list('pk', flat=True)
    hotels_with_one_room = Hotel.objects.filter(id__in=hotels_list).values('title')
    return JsonResponse({'hotels_with_only_one': list(hotels_with_one_room)})