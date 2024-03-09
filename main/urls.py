from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import book_appointment, appointments_view, send_enquiry, view_enquiries, doctor_appointments, update_appointment, patient_enquiries, donate_view, AppointmentListCreateAPIView, EnquiryListCreateAPIView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('appointments/', appointments_view, name='appointments_view'),
    path('send-enquiry/', send_enquiry, name='send_enquiry'),
    path('view-enquiries/', view_enquiries, name='view_enquiries'),
    path('patient-enquiries/', patient_enquiries, name='patient_enquiries'),
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('update-appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('donate/', donate_view, name='donate'),
    
    #API
    path('api/donations/', views.donation_create, name='api_donation_create'),
    path('api/appointments/', AppointmentListCreateAPIView.as_view(), name='appointment-list-create'),
    path('api/enquiries/', EnquiryListCreateAPIView.as_view(), name='enquiry-list-create'),
]

