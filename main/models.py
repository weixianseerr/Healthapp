from django.db import models
from django.contrib.auth.models import User

#User Role
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " - " + ("Doctor" if self.is_doctor else "Patient")

#Appointment
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)
    rescheduled_date = models.DateField(null=True, blank=True)
    rescheduled_time = models.TimeField(null=True, blank=True)
   
    def __str__(self):
        return f"{self.patient.username}'s appointment with {self.doctor.username} on {self.date} at {self.time}"
    
#Enquires
class Enquiry(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_enquiries')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_enquiries')
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Enquiry from {self.patient.username}"

#Donate 
class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='donations')
    amount_wei = models.BigIntegerField()  # Amount in Wei
    amount_eth = models.DecimalField(max_digits=18, decimal_places=8)  # Converted amount in Ether
    transaction_hash = models.CharField(max_length=66)  # Length of an Ethereum transaction hash
    sender_address = models.CharField(max_length=42)  # Length of an Ethereum address
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    # Additional fields for validation
    block_number = models.IntegerField(null=True, blank=True)
    confirmation_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Donation by {self.donor.username if self.donor else 'Anonymous'} on {self.timestamp}"

    