from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    title = models.CharField(max_length=128)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f'Hotel - {self.pk}'


class Room(models.Model):
    title = models.CharField(max_length=128)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    # добавление атрибута к модели, но не допер как использовать его в queryset
    @property
    def rooms_sold_out(self):
        if self.reservations:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.hotel.title} - Room - {self.pk}'


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f'Reserved: {self.room} at {self.user.username}'