from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Donation, Appointment, Enquiry
from decimal import Decimal

#Donation Testcase
class DonationTests(APITestCase):
    def test_create_donation(self):
        """
        Ensure we can create a new donation object.
        """
        url = reverse('api_donation_create')
        data = {
            'amount_wei': 1000000000000000000,  # Equivalent to 1 Ether in Wei
            'amount_eth': '1.00', 
            'transaction_hash': '0xSomeHash',
            'sender_address': '0xSomeSenderAddress'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donation.objects.count(), 1)
        self.assertEqual(Donation.objects.get().amount_eth, Decimal('1.00'))

#Appointment Testcase
class AppointmentAPITests(APITestCase):
    def test_create_appointment(self):
        """
        Ensure we can create a new appointment object via the API.
        """
        # Setup test users
        patient_user = User.objects.create_user(username='patient', password='testpass')
        doctor_user = User.objects.create_user(username='doctor', password='testpass')
        self.client.login(username='patient', password='testpass')

        url = reverse('appointment-list-create')
        data = {
            'patient': patient_user.id,
            'doctor': doctor_user.id,
            'date': '2024-01-01',
            'time': '09:00:00',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.get().patient.username, 'patient')
        self.assertEqual(Appointment.objects.get().doctor.username, 'doctor')

#Enquires Testcase
class EnquiryAPITests(APITestCase):
    def test_create_enquiry(self):
        """
        Ensure we can create a new enquiry object via the API.
        """
        patient_user = User.objects.create_user(username='patient', password='testpass')
        doctor_user = User.objects.create_user(username='doctor', password='testpass')
        self.client.login(username='patient', password='testpass')

        url = reverse('enquiry-list-create')
        data = {
            'patient': patient_user.id,
            'doctor': doctor_user.id,
            'message': 'I need some medical advice.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enquiry.objects.count(), 1)
        self.assertEqual(Enquiry.objects.get().patient.username, 'patient')
        self.assertEqual(Enquiry.objects.get().message, 'I need some medical advice.')


