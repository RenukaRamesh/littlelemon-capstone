from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registration/', views.register, name='registration'),

    # API endpoints
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('api/menu/<int:pk>/', views.MenuItemView.as_view(), name='menu-detail'),
    path('api/bookings/', views.BookingViewSet.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
]
