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
                payment_status="paid",  # Set the payment status as "pending" initially
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


from django.shortcuts import render
from django.http import HttpResponse
# from .models import Film, Review, Audience, Rating
from django.utils.timezone import now

def use_add_rating(request, film_id):
    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review']
        login_id = request.session['login_id']
        
        # Fetch film and audience details
        film_res = film.objects.get(pk=film_id)
        audience = Audience.objects.get(pk=login_id)  # Assuming login_id corresponds to an Audience
        
        # Save the rating
        # Review.objects.create(rating=rating, film=film_res, audience=audience)  # Assuming Login and Audience are related
        
        # Save the review
        Review.objects.create(
            audience=audience,
            film=film_res,
            rating=rating,
            review_text=review_text,
            review_date=now()
        )
        
        return HttpResponse("<script>alert('Rating & Review Added Successfully');window.location='/user_home';</script>")

    return render(request, 'use_add_rating.html')

# from django.shortcuts import render
# from .models import SeatBooking

def user_view_booked_tickets(request):
    login_id = request.session.get('login_id')  # Assuming the logged-in user ID is stored in the session

    audience_res = Audience.objects.get(login_id=login_id)

    # Fetch booked tickets for the logged-in audience
    booked_tickets = SeatBooking.objects.filter(audience=audience_res).select_related('slot__film', 'slot__theater', 'seat')

    context = {
        'booked_tickets': booked_tickets
    }

    return render(request, 'user_view_booked_tickets.html', context)



#######################################film maker
from django.core.files.storage import FileSystemStorage

def filmaker_reg(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']  
        phone = request.POST['phone']
        password = request.POST['password']
        photo = request.FILES['prof_img']

        # photo=request.FILES['photo']
        


        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)


        bio = request.POST['bio']
        username = request.POST['username']

        try:
            lg=Login.objects.get(username=username,password=password)
            if lg:
                return HttpResponse("<script>alert('UserName Already Exist');window.location='/filmaker_reg';</script>")
        except:
            lg=Login(username=username,password=password,usertype='film_maker')
            lg.save()

            fm=Filmmaker(name=name,email=email,phone=phone,profile_image=image,bio=bio,login=lg)
            fm.save()
            return HttpResponse("<script>alert('Filmaker Added Successfully');window.location='/login';</script>")
    return render(request,'filmaker_reg.html')


def filmaker_home(request):
    films = film.objects.all()
    return render(request,'filmaker_home.html',{'films':films})


def filmmaker_view_prof(request):
    maker = Filmmaker.objects.filter(login=request.session['login_id'])
    return render(request,'filmmaker_view_prof.html',{'maker':maker})


def film_maker_view_theaters(request):  
    theaters = Theater.objects.all()
    screening_slots = ScreeningSlot.objects.all()  
    return render(request,'film_maker_view_theaters.html',{'theaters':theaters, 'screening_slots': screening_slots})


def film_maker_book_seats(request, theater_id, screening_slot_id):
    # Fetch seats related to the selected screening slot
    seats = TheaterSeat.objects.filter(slot_id=screening_slot_id)

    return render(request, 'film_maker_book_seats.html', {'seats': seats, 'screening_slot_id': screening_slot_id})



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# from .models import TheaterSeat, SeatBooking, ScreeningSlot

@csrf_exempt  # Use if you're not handling CSRF tokens in your frontend (not recommended for production)
def film_maker_seat_confirm(request):
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
        aud_id=Filmmaker.objects.get(login_id=request.session['login_id'])
        booked_seats = []
        for seat in seats_to_book:
            # Create a SeatBooking entry for each seat
            SeatBooking.objects.create(
                slot=screening_slot,
                seat=seat,
                audience=None,  # You can set this to the audience if applicable
                filmmaker=aud_id,  # You can set this to the filmmaker if applicable
                payment_status="paid",  # Set the payment status as "pending" initially
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


def film_maker_view_campaigns(request):
    films = film.objects.filter(filmmaker=request.session['fm_id'])
    return render(request,'film_maker_view_campaigns.html',{'films':films})
    # return render(request,'film_maker_view_campaigns.html')

# def film_maker_view_campaigns_basedon_films(request,film_id):
#     campaigns = MarketingCampaign.objects.filter(film=film_id)
#     return render(request,'film_maker_view_campaigns_basedon_films.html',{'campaigns':campaigns})


def film_maker_view_campaigns_basedon_films(request, film_id):
    campaigns = MarketingCampaign.objects.filter(film=film_id)

    # Fetch related Ad data for each campaign
    # campaign_data = []
    # for campaign in campaigns:
    #     ads = Ad.objects.filter(campaign=campaign)
    #     for ad in ads:
    #         campaign_data.append({
    #             'start_date': campaign.start_date,
    #             'end_date': campaign.end_date,
    #             'budget': campaign.budget,
    #             'status': campaign.status,
    #             'target_audience': ad.target_audience,
    #             'platform': ad.platform,
    #             'impressions': ad.impressions,
    #             'clicks': ad.clicks
    #         })

    return render(request, 'film_maker_view_campaigns_basedon_films.html', {'campaigns': campaigns})




def film_update_profile(request,id):
    a=Filmmaker.objects.get(filmmaker_id=id)
    if'submit'in request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        bio=request.POST['bio']

        a.name=name
        a.email=email
        a.phone=phone
        a.bio=bio

        a.save()
        return HttpResponse("<script>alert('FILMAKER PRODFILE UPDATED');window.location='/filmmaker_view_prof';</script>")



    return render(request,"film_update_profile.html",{'a':a})

# from django.shortcuts import render
# from .models import Chat, TheaterOwner, Login

def film_maker_view_mssges(request):
    # Get all chat messages
    chats = chat.objects.all()

    # Extract unique login_ids from 'fromid' and 'toid' fields
    theater_owner_login_ids = set(chats.values_list('fromid', flat=True)) | set(chats.values_list('toid', flat=True))

    # Fetch TheaterOwner details where login_id matches 'fromid' or 'toid'
    theater_owners = TheaterOwner.objects.filter(login__login_id__in=theater_owner_login_ids).values(
        'owner_id', 'name', 'email', 'phone', 'profile_image', 'login__login_id'
    )

    return render(request, 'film_maker_view_mssges.html', {'theater_owners': theater_owners})


# from django.shortcuts import render, redirect
# # from .models import Chat, Login, TheaterOwner
# from django.db.models import Q
# from django.utils.timezone import now

# def film_maker_chat_owners(request, login_id):
#     sender_id = request.session.get('login_id')  # Filmmaker's login ID
#     receiver_id = login_id  # Theater owner's login ID
    
#     # Fetch chat messages (both sent & received)
#     messages = chat.objects.filter(
#         (Q(fromid=sender_id, toid=receiver_id) | Q(fromid=receiver_id, toid=sender_id))
#     ).order_by('chatid')

#     # Handle message sending
#     if request.method == "POST":
#         message_text = request.POST.get('message')
#         if message_text:
#             chat.objects.create(fromid=sender_id, toid=receiver_id, date=now(), message=message_text)
#             return redirect('film_maker_chat_owners', login_id=receiver_id)  # Refresh the page

#     # Fetch theater owner details
#     theater_owner = TheaterOwner.objects.get(login__login_id=receiver_id)

#     return render(request, 'film_maker_chat_owners.html', {
#         'messages': messages,
#         'theater_owner': theater_owner,
#         'sender_id': sender_id
#     })

from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.timezone import now
# from .models import Chat, TheaterOwner

def film_maker_chat_owners(request, login_id):
    sender_id = request.session.get('login_id')  # Filmmaker's login ID
    receiver_id = login_id  # Theater owner's login ID
    
    # Fetch chat messages (both sent & received)
    messages = chat.objects.filter(
        Q(fromid=sender_id, toid=receiver_id) | Q(fromid=receiver_id, toid=sender_id)
    ).order_by('date')  # Order messages by date (ensure it's the correct field for ordering)

    # Handle message sending
    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            chat.objects.create(fromid=sender_id, toid=receiver_id, date=now(), message=message_text)
            return redirect('film_maker_chat_owners', login_id=receiver_id)  # Refresh the page

    # Fetch theater owner details
    theater_owner = TheaterOwner.objects.get(login__login_id=receiver_id)

    return render(request, 'film_maker_chat_owners.html', {
        'messages': messages,
        'theater_owner': theater_owner,
        'sender_id': sender_id
    })


def film_maker_view_tickets(request):
    login_id = request.session.get('login_id')  # Assuming the logged-in user ID is stored in the session

    audience_res = Filmmaker.objects.get(login_id=login_id)

    # Fetch booked tickets for the logged-in audience
    booked_tickets = SeatBooking.objects.filter(filmmaker=audience_res).select_related('slot__film', 'slot__theater', 'seat')

    context = {
        'booked_tickets': booked_tickets
    }

    return render(request, 'film_maker_view_tickets.html', context)


###########################content manager############################3
def content_manager_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']  
        phone = request.POST['phone']
        password = request.POST['password']
        photo = request.FILES['profile_image']

        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)

        username = request.POST['username']

        try:
            lg = Login.objects.get(username=username, password=password)
            if lg:
                return HttpResponse("<script>alert('UserName Already Exist');window.location='/signup';</script>")
        except Login.DoesNotExist:
            lg = Login(username=username, password=password, usertype='content_manager')
            lg.save()

            cm = ContentManager(name=name, email=email, phone=phone, profile_image=image, login=lg)
            cm.save()
            return HttpResponse("<script>alert('Content Manager Added Successfully');window.location='/login';</script>")

    return render(request,"content_manager_reg.html")


def content_manager_home(request):
    return render(request,"content_manager_home.html")


def conter_manager_view_prof(request):
    manager = ContentManager.objects.filter(login=request.session['login_id'])
    return render(request,'conter_manager_view_prof.html',{'maker':manager})


# def conter_manager_view_films_to_make_campaign(request):
#     films = film.objects.all()
#     # return render(request,'filmaker_home.html',{'films':films})
#     return render(request,"conter_manager_view_films_to_make_campaign.html",{'films':films})

def conter_manager_view_films_to_make_campaign(request):
    films = film.objects.select_related('filmmaker').all()
    return render(request, "conter_manager_view_films_to_make_campaign.html", {'films': films})


def content_manager_manage_campaigns(request, film_id, film_m_id):
    campaign_data= MarketingCampaign.objects.filter(film=film_id)
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        budget = request.POST['budget']
        status = request.POST['status']

        try:
            filmmaker = Filmmaker.objects.get(pk=film_m_id)
            film_data = film.objects.get(pk=film_id)
            manager = ContentManager.objects.first()  # Change this to get the logged-in manager

            # Create and save the marketing campaign
            campaign = MarketingCampaign(
                filmmaker=filmmaker,
                film=film_data,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                status=status,
                manager=manager
            )
            campaign.save()

            return HttpResponse("<script>alert('Campaign Created Successfully'); window.location='/conter_manager_view_films_to_make_campaign';</script>")

        except Filmmaker.DoesNotExist:
            return HttpResponse("<script>alert('Filmmaker Not Found'); window.history.back();</script>")
        except film.DoesNotExist:
            return HttpResponse("<script>alert('Film Not Found'); window.history.back();</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}'); window.history.back();</script>")

    return render(request, "content_manager_manage_campaigns.html", {"film_id": film_id, "film_m_id": film_m_id, "camp_films_data":campaign_data})


# from django.contrib import messages

def update_campaign(request,cam_id):
    campaign_data= MarketingCampaign.objects.get(pk=cam_id)
    # print(campaign_data,"********")

    if request.method == 'POST':
        # Get data from the form
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        budget = request.POST.get('budget')
        status = request.POST.get('status')

        # Update the campaign object with new values
        campaign_data.start_date = start_date
        campaign_data.end_date = end_date
        campaign_data.budget = budget
        campaign_data.status = status

        # Save the updated object to the database
        campaign_data.save()
        return HttpResponse("<script>alert('Updated successfully'); window.location='/conter_manager_view_films_to_make_campaign';</script>")

    return render(request,"update_campaign.html",{ "camp_films_data":campaign_data})


from django.shortcuts import render
# from .models import Review, Film, Filmmaker

def content_manager_view_reviewratings(request, filmid):
    film_reviews = Review.objects.filter(film_id=filmid).select_related('film', 'audience')

    context = {'film_reviews': film_reviews}
    return render(request, "content_manager_view_reviewratings.html", context)
