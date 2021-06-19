"""june_homes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotelapp.views import (
    dislike_hotel_view,
    like_hotel_view,
    get_all_guests_in_hotel,
    get_list_of_hotels_with_only_one_free_room,
    get_rooms_list_with_sold_out_sign,
    index
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('dislike_hotel/<int:hotel_id>/', dislike_hotel_view, name='dislike_hotels'),
    path('like_hotel/<int:hotel_id>/', like_hotel_view, name='like_hotels'),
    path('hotel_guests/<str:hotel_name>/', get_all_guests_in_hotel, name='get_guests'),
    path('only_one/', get_list_of_hotels_with_only_one_free_room, name='only_one'),
    path('sold_out/<str:move_in>/<str:move_out>/', get_rooms_list_with_sold_out_sign, name='sold_out'),
]
