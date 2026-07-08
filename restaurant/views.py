import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
from rest_framework import generics
from .serializers import MenuSerializer, BookingSerializer
from .models import Menu
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username taken'}, status=400)
    User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created'}, status=201)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

def book(request):
    date_str = request.GET.get('date') or request.POST.get('date')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        no_of_guests = request.POST.get('no_of_guests')
        reservation_date = request.POST.get('reservation_date')
        reservation_slot = request.POST.get('reservation_slot')

        exists = Booking.objects.filter(
            reservation_date=reservation_date,
            reservation_slot=reservation_slot
        ).exists()

        if exists:
            bookings = Booking.objects.filter(reservation_date=reservation_date)
            return render(request, 'book.html', {
                'error': 'Slot already booked. Please choose another time.',
                'bookings': bookings,
                'selected_date': reservation_date,
            })

        Booking.objects.create(
            first_name=first_name,
            no_of_guests=int(no_of_guests) if no_of_guests else 1,
            reservation_date=reservation_date,
            reservation_slot=reservation_slot
        )
        bookings = Booking.objects.filter(reservation_date=reservation_date)
        return render(request, 'book.html', {
            'success': 'Booking confirmed!',
            'bookings': bookings,
            'selected_date': reservation_date,
        })

    # GET request
    if date_str:
        bookings = Booking.objects.filter(reservation_date=date_str)
        booked_slots = list(bookings.values_list('reservation_slot', flat=True))
        booked_slots = [str(s)[:8] for s in booked_slots]
    else:
        bookings = Booking.objects.none()
        booked_slots = []

    return render(request, 'book.html', {
        'bookings': bookings,
        'selected_date': date_str or '',
        'booked_slots': booked_slots,
    })

def bookings_api(request):
    date_str = request.GET.get('date')
    if date_str:
        bookings = Booking.objects.filter(reservation_date=date_str)
    else:
        bookings = Booking.objects.all()

    data = list(bookings.values('id', 'first_name', 'no_of_guests', 'reservation_date', 'reservation_slot'))
    for b in data:
        b['reservation_date'] = str(b['reservation_date'])
        b['reservation_slot'] = str(b['reservation_slot'])
    return JsonResponse(data, safe=False)

def reservations(request):
    bookings = Booking.objects.all()
    data = list(bookings.values('id', 'first_name', 'no_of_guests', 'reservation_date', 'reservation_slot'))
    for b in data:
        b['reservation_date'] = str(b['reservation_date'])
        b['reservation_slot'] = str(b['reservation_slot'])
    return JsonResponse(data, safe=False)

class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class BookingViewSet(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer