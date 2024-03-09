from rest_framework import serializers
from .models import Donation, Appointment, Enquiry

#Donation
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'donor', 'amount_wei', 'amount_eth', 'transaction_hash', 'sender_address', 'timestamp', 'status']

#Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

#Enquires
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'