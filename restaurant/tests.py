from django.test import TestCase
from django.contrib.auth.models import User
from .models import Menu, Booking

class MenuModelTest(TestCase):
    def test_create_menu_item(self):
        item = Menu.objects.create(title="Pizza", price=12.99, inventory=10)
        self.assertEqual(str(item), "Pizza")
        self.assertEqual(Menu.objects.count(), 1)

class BookingModelTest(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(
            first_name="John",
            no_of_guests=4,
            reservation_date="2026-08-01",
            reservation_slot="19:00:00"
        )
        self.assertEqual(Booking.objects.count(), 1)

class MenuAPITest(TestCase):
    def test_get_menu_list(self):
        Menu.objects.create(title="Burger", price=8.99, inventory=5)
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)

class RegistrationAPITest(TestCase):
    def test_register_user(self):
        response = self.client.post('/api/registration/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 201)