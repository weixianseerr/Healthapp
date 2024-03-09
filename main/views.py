from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, AppointmentForm, EnquiryForm, EnquiryResponseForm, AppointmentUpdateForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Appointment, Enquiry, Donation
from django.http import JsonResponse
import requests
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DonationSerializer, AppointmentSerializer, EnquirySerializer

#Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if UserProfile already exists
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_doctor = form.cleaned_data['is_doctor']
            profile.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

#Home
from django.shortcuts import render
from .models import Donation

def home(request):
    # Fetch the latest 10 donations
    latest_donations = Donation.objects.order_by('-timestamp')[:10]

    #News
    medical_news = [
        {
        "title": "Ongoing COVID-19 Pandemic",
        "content": "Vaccination rates continue to improve globally. Health officials remind the public to stay vigilant with hygiene practices and to respect local health guidelines. Booster shots are now available for increased protection.",
        "date": "2024-02-25"
        },
        {
        "title": "Seasonal Flu on the Rise",
        "content": "With the changing seasons, health professionals report an uptick in flu cases. Getting the flu vaccine can reduce the risk of severe symptoms and help protect vulnerable populations.",
        "date": "2024-03-01"
        },
        {
        "title": "Heart Health Awareness Month",
        "content": "February marks Heart Health Awareness month. Doctors encourage regular exercise, a balanced diet, and routine check-ups to prevent heart disease and maintain a healthy lifestyle.",
        "date": "2024-02-01"
        },
        {
        "title": "Mental Health in the Workplace",
        "content": "Companies are increasingly recognizing the importance of mental health and are incorporating wellness programs to support employees, including access to counseling services and mental health days.",
        "date": "2024-04-10"
        },
        {
        "title": "Advancements in Telemedicine",
        "content": "Telemedicine is becoming a staple in providing accessible healthcare. New technologies are emerging that offer patients high-quality care from the comfort of their homes.",
        "date": "2024-01-15"
        },
        {
        "title": "New Study on the Benefits of Mediterranean Diet",
        "content": "Researchers find a link between the Mediterranean diet and improved cognitive function. The diet, rich in fruits, vegetables, and healthy fats, continues to show a variety of health benefits.",
        "date": "2024-03-22"
        },
        {
        "title": "Global Efforts to Combat Malaria",
        "content": "Recent initiatives have shown promise in reducing the incidence of malaria in several high-risk regions. Continued efforts and funding are crucial to sustain these positive trends.",
        "date": "2024-04-25"
        },
        {
        "title": "Awareness Campaign for Diabetes Prevention",
        "content": "A new campaign focuses on diabetes prevention through education on risk factors, early detection, and lifestyle modifications. Free screenings are available at participating clinics.",
        "date": "2024-05-05"
        },
        {
        "title": "Rise of Allergies in Urban Areas",
        "content": "Studies indicate a rise in allergy cases in urban areas due to pollution and climate change. Experts suggest practical steps to manage symptoms and reduce exposure to allergens.",
        "date": "2024-05-18"
        },
        {
        "title": "Breakthrough in Alzheimer's Research",
        "content": "Scientists announce a breakthrough in Alzheimer's research, offering new insights into potential treatments. The study focuses on early detection and preventive strategies.",
        "date": "2024-06-30"
        },
        
    ]

    context = {
        'is_authenticated': request.user.is_authenticated,
        'latest_donations': latest_donations,
        'medical_news': medical_news,
        'username': request.user.username if request.user.is_authenticated else 'Guest'
    }

    return render(request, 'main/home.html', context)


#Booking Appointment (Patients)
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('appointments_view')  # Redirect to the appointment view page
    else:
        form = AppointmentForm()
    return render(request, 'main/book_appointment.html', {'form': form})

#Logged in View appointment (patients)
@login_required
def appointments_view(request):
    if request.user.userprofile.is_doctor:
        return redirect('home')  # Redirect doctors to homepage

    patient_appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'time')
    return render(request, 'main/view_appointments.html', {'appointments': patient_appointments})

#Viewing Appointment(Doctor)
@login_required
def doctor_appointments(request):
    if not request.user.userprofile.is_doctor:
        return redirect('home')  #redirct to home

    appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
    return render(request, 'main/doctor_appointments.html', {'appointments': appointments})

#For doctor to update the appointment
@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    form = AppointmentUpdateForm(instance=appointment)

    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            if form.cleaned_data['confirm']:
                appointment.confirmed = True
            if form.cleaned_data['reschedule']:
                appointment.rescheduled_date = form.cleaned_data['rescheduled_date']
                appointment.rescheduled_time = form.cleaned_data['rescheduled_time']
                appointment.save()
            return redirect('doctor_appointments')
    
    return render(request, 'main/update_appointment.html', {'form': form, 'appointment': appointment})




#Sending Enquires patient to doctor 
@login_required
def send_enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.patient = request.user
            enquiry.save()
            return redirect('home')  # Redirect to home
    else:
        form = EnquiryForm()
    return render(request, 'main/send_enquiry.html', {'form': form})

#Viewing Enquires and reponse for doctor 
@login_required
def view_enquiries(request):
    if not request.user.userprofile.is_doctor:
        return redirect('home')  # Redirect to home

    enquiries = Enquiry.objects.filter(doctor=request.user)
    
    if request.method == 'POST':
        enquiry_id = request.POST.get('enquiry_id')
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = EnquiryResponseForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            return redirect('view_enquiries')
    else:
        for enquiry in enquiries:
            enquiry.form = EnquiryResponseForm(instance=enquiry)  # Attach the form to each enquiry

    return render(request, 'main/view_enquiries.html', {'enquiries': enquiries})

#patient seeing responded enquires from doctor 
@login_required
def patient_enquiries(request):
    if request.user.userprofile.is_doctor:
        return redirect('home')  # Redirect doctors to a home page

    user_enquiries = Enquiry.objects.filter(patient=request.user).order_by('-created_at')
    return render(request, 'main/patient_enquiries.html', {'enquiries': user_enquiries})

#chat
@login_required
def contact_us(request):
    # A general room name for all users
    room_name = 'general_contact_us'
    
    return render(request, 'main/chat.html', {
        'room_name': room_name,
        'username': request.user.username  #display who sent a message
    })

#Donation
def donate_view(request):
    return render(request, 'main/donate.html')

@login_required
def record_donation(request):
    if request.method == 'POST':
        txn_hash = request.POST.get('txn_hash')
        amount = request.POST.get('amount')
        sender_address = request.POST.get('sender_address')
        
        # Verify the transaction using Etherscan API
        txn_status = get_transaction_status(txn_hash)
        if txn_status == '1':  # Check if the transaction was successful
            Donation.objects.create(
                donor=request.user,
                amount=amount,
                transaction_hash=txn_hash,
                sender_address=sender_address
            )
            return JsonResponse({'status': 'success', 'txn_hash': txn_hash})
        else:
            return JsonResponse({'status': 'error', 'message': 'Transaction failed or not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


#verify donation transaction 
def get_transaction_status(txn_hash):
    api_key = '' #your own API
    url = f'https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={txn_hash}&apikey={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['result']['status']  # '1' means success, '0' means failure
    else:
        return None
    

#REST API
#Donation
@api_view(['POST'])
def donation_create(request):
    if request.method == 'POST':
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Appointment
class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

#Enquires
class EnquiryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer