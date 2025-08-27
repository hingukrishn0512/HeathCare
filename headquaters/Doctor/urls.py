from django.urls import path
from .import views

urlpatterns = [
    path('', views.landing , name='landing'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('register/', views.register , name='register'),
    path('account/login', views.login , name='account'),
    path('doctors/', views.doctors , name='doctor'),
    path('profile/', views.profile , name='profile'),
    path('appointment/<int:id>', views.appointment , name='appointment'),
    path('bookings/', views.bookings , name='booked'),
    path('generator/', views.generator_ai , name='generator'),
    path('edit/<int:id>', views.edit_slots , name='edit'),
    path('thanks/', views.thanks , name='thanks'),
    path('home/', views.home , name='home'),
    path('bookings/home/', views.home , name='booking_home'),
    path('thanks/home/', views.home , name='thanks_home'),

    




    
]
