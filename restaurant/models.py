from django.db import models

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    no_of_guests = models.IntegerField()
    reservation_date = models.DateField()
    reservation_slot = models.TimeField(default="19:00:00")

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} {self.reservation_slot}"

class Menu(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()

    def __str__(self):
        return self.title