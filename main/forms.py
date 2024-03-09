from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Appointment, UserProfile, Enquiry
import datetime

#Register
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_doctor = forms.BooleanField(required=False, label='Register as Doctor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_doctor']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, is_doctor=self.cleaned_data['is_doctor'])
            user_profile.save()
        return user

#Sending Appointment to Doctor 
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(userprofile__is_doctor=True)

#Doctor updating appointments
class AppointmentUpdateForm(forms.ModelForm):
    confirm = forms.BooleanField(required=False, label='Confirm Appointment')
    reschedule = forms.BooleanField(required=False, label='Reschedule Appointment')
    rescheduled_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}))
    rescheduled_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['confirm', 'reschedule', 'rescheduled_date', 'rescheduled_time']

    def clean(self):
        cleaned_data = super().clean()
        confirm = cleaned_data.get("confirm")
        reschedule = cleaned_data.get("reschedule")
        rescheduled_date = cleaned_data.get("rescheduled_date")
        rescheduled_time = cleaned_data.get("rescheduled_time")

        if reschedule and (not rescheduled_date or not rescheduled_time):
            raise forms.ValidationError("Please provide both date and time for rescheduling.")

        if confirm and reschedule:
            raise forms.ValidationError("An appointment cannot be confirmed and rescheduled at the same time.")

        return cleaned_data

#Sending Enquires to Doctor 
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['doctor', 'message']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        # Filter the queryset to only include doctors
        self.fields['doctor'].queryset = User.objects.filter(userprofile__is_doctor=True)

#Doctor Reponse to enquires
class EnquiryResponseForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['response']