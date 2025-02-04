from django.shortcuts import render
from bridgeApp.models import *
from django.http import *
from datetime import date


# Create your views here.
def user_home(request):
    films = film.objects.all()
    return render(request,'user_home.html',{'films':films})

def user_reg(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']  
        phone = request.POST['phone']
        preferences = request.POST['preferences']  # Added preferences field
        username = request.POST['username']  # Added username field
        password = request.POST['password']  # Corrected 'pass' to 'password'


        try:
            lg=Login.objects.get(username=username,password=password)
            if lg:
                return HttpResponse("<script>alert('UserName Already Exist');window.location='/user_reg';</script>")
        except:
            lg=Login(username=username,password=password,usertype='user')
            lg.save()

            aud=Audience(name=name,email=email,phone=phone,login=lg)
            aud.save()
            return HttpResponse("<script>alert('User Added Successfully');window.location='/login';</script>")
    return render(request,'user_reg.html')


def user_view_nots(request):    
    nots = notification.objects.all()
    return render(request,'user_view_nots.html',{'nots':nots})


def user_send_complaints(request):
    try:
        comp=complaint.objects.filter(senderid=request.session['login_id'])
        print("GGGGGGGGGGGGGGGGGGGGGG")
    except:
        comp=None
    if request.method=='POST':
        com_plaint = request.POST['complaint']

        login_id = Login.objects.get(login_id=request.session['login_id'])


        comp=complaint(complaint=com_plaint,reply='pending',date=date.today(),senderid=login_id)
        comp.save()
        return HttpResponse("<script>alert('Complaint Send Successfully');window.location='/user_send_complaints';</script>")
    return render(request,'user_send_complaints.html',{'complaints':comp})


def user_view_theaters(request):
    theaters = Theater.objects.all()
    screening_slots = ScreeningSlot.objects.all()
    return render(request,'user_view_theaters.html',{'theaters':theaters, 'screening_slots': screening_slots})


def user_book_seats(request, theater_id, screening_slot_id):
    # Fetch seats related to the selected screening slot
    seats = TheaterSeat.objects.filter(slot_id=screening_slot_id)

    return render(request, 'user_book_seats.html', {'seats': seats, 'screening_slot_id': screening_slot_id})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# from .models import TheaterSeat, SeatBooking, ScreeningSlot

@csrf_exempt  # Use if you're not handling CSRF tokens in your frontend (not recommended for production)
def user_seat_confirm(request):
    if request.method == "POST":
        # Parse the incoming JSON data from the frontend
        data = json.loads(request.body)
        selected_seats = data.get("seats", [])
        total_amount = data.get("total_amount", 0)
        screening_slot_id = data.get("screening_slot_id")

        print(selected_seats, "&&&&&&&&&&&&&&&")

        # Fetch the screening slot from the database using the correct field (assuming slot_id is the correct field)
        try:
            screening_slot = ScreeningSlot.objects.get(slot_id=screening_slot_id)  # Use slot_id instead of id
        except ScreeningSlot.DoesNotExist:
            return JsonResponse({"success": False, "error": "Screening slot not found."})

        # Check if all seats exist and are available
        seats_to_book = []
        unavailable_seats = []
        
        for seat_id in selected_seats:
            try:
                seat = TheaterSeat.objects.get(seat_id=seat_id, status="available")  # Ensure the seat is available
                seats_to_book.append(seat)
                print(seats_to_book, "((((((((()))))))))")
            except TheaterSeat.DoesNotExist:
                # If any seat doesn't exist or isn't available, add to the unavailable list
                unavailable_seats.append(seat_id)

        # If there are unavailable seats, return an error message
        if unavailable_seats:
            return JsonResponse({"success": False, "error": f"Seats {', '.join(map(str, unavailable_seats))} are not available or do not exist."})

        # Proceed with booking the seats
        aud_id=Audience.objects.get(login_id=request.session['login_id'])
        booked_seats = []
        for seat in seats_to_book:
            # Create a SeatBooking entry for each seat
            SeatBooking.objects.create(
                slot=screening_slot,
                seat=seat,
                audience=aud_id,  # You can set this to the audience if applicable
                filmmaker=None,  # You can set this to the filmmaker if applicable
                payment_status="pending",  # Set the payment status as "pending" initially
                booking_date=timezone.now()  # Set the booking date to the current time
            )
            seat.status = "booked"  # Mark each seat as booked
            seat.save()
            booked_seats.append(seat.seat_id)  # Add the seat_id to the list of booked seats

        # Optionally, you can store the booking transaction in a separate model, if needed
        # For example, you can create a Booking object here if you want to track the entire booking process.

        return JsonResponse({
            "success": True, 
            "message": "Seats booked successfully!", 
            "booked_seats": booked_seats,  # Optionally return the booked seats
            "total_amount": total_amount  # Optionally return the total amount for the booking
        })

    return JsonResponse({"success": False, "error": "Invalid request"})

