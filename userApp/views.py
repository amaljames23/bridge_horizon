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
    seats = TheaterSeat.objects.filter(slot_id=screening_slot_id,theater_id=theater_id)

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

            owner_id = screening_slot.theater.owner_id

            owner_l_id = Login.objects.get(pk=owner_id)
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

        local_time = timezone.localtime(timezone.now())

        # If there are unavailable seats, return an error message
        if unavailable_seats:
            return JsonResponse({"success": False, "error": f"Seats {', '.join(map(str, unavailable_seats))} are not available or do not exist."})

        # Proceed with booking the seats
        aud_id=Audience.objects.get(login_id=request.session['login_id'])
        booked_seats = []
        for seat in seats_to_book:
            # Create a SeatBooking entry for each seat
            booking = SeatBooking.objects.create(
                slot=screening_slot,
                seat=seat,
                audience=aud_id,  # You can set this to the audience if applicable
                filmmaker=None,  # You can set this to the filmmaker if applicable
                payment_status="paid",  # Set the payment status as "pending" initially
                booking_date=timezone.now()  # Set the booking date to the current time
            )

            Payment.objects.create(
                booking=booking,
                payer=aud_id.login,  # Set the payer (user making the payment)
                receiver=owner_l_id,  # Set the receiver (e.g., filmmaker or admin)
                amount=total_amount,  # Assuming seat has a price attribute
                transaction_date=local_time,
                status="completed"  # Set payment status
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


from django.db.models import Count
# from django.shortcuts import render
# from your_app.models import Film

def user_view_film_recommendations(request):
    # Get films ranked by number of bookings
    
    films_ranked = film.objects.annotate(
        booking_count=Count('screeningslot__seatbooking')
    ).order_by('-booking_count')

    # Pass the ranked films to the template
    return render(request, 'user_view_film_recommendations.html', {'films_ranked': films_ranked})


def user_view_promotion_details(request, filmid):
    # film_res = get_object_or_404(film, film_id=filmid)
    
    # Fetch only accepted promo materials
    promo_materials = PromoMaterial.objects.filter(film_id=filmid, status="Accepted")

    return render(request, 'user_view_promotion_details.html', {
        'film_res': filmid,
        'promo_materials': promo_materials
    })



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


def film_maker_view_theaters(request,film_id):  
    theaters = Theater.objects.all()
    screening_slots = ScreeningSlot.objects.all()  
    return render(request,'film_maker_view_theaters.html',{'theaters':theaters, 'screening_slots': screening_slots,'film_id':film_id})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
# from .models import BookTheaters
import datetime 
def film_maker_book_theater(request, theater_id, film_id):
    # if request.method == "POST":
        # Get today's date in 'YYYY-MM-DD' format
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')

        # Insert into BookTheaters model
        BookTheaters.objects.create(
            film_id=film_id,
            theater_id=theater_id,
            date=today_date,  # Using today's date
            fimmaker_id=request.session['fm_id'],  # Fetch filmmaker ID from session
            status="Pending"  # Default status
        )

        # Return JavaScript alert and redirect
        return HttpResponse("<script>alert('Booked Successfully');window.location='/filmaker_home';</script>")

    # return HttpResponse("<script>alert('Invalid Request');window.history.back();</script>")




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

            owner_id = screening_slot.theater.owner_id

            owner_l_id = Login.objects.get(pk=owner_id)
            
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

        local_time = timezone.localtime(timezone.now())

        # If there are unavailable seats, return an error message
        if unavailable_seats:
            return JsonResponse({"success": False, "error": f"Seats {', '.join(map(str, unavailable_seats))} are not available or do not exist."})

        # Proceed with booking the seats
        aud_id=Filmmaker.objects.get(login_id=request.session['login_id'])
        booked_seats = []
        for seat in seats_to_book:
            # Create a SeatBooking entry for each seat
            booking = SeatBooking.objects.create(
                slot=screening_slot,
                seat=seat,
                audience=None,  # You can set this to the audience if applicable
                filmmaker=aud_id,  # You can set this to the filmmaker if applicable
                payment_status="paid",  # Set the payment status as "pending" initially
                booking_date=local_time  # Set the booking date to the current time
            )

            Payment.objects.create(
                booking=booking,
                payer=aud_id.login,  # Set the payer (user making the payment)
                receiver=owner_l_id,  # Set the receiver (e.g., filmmaker or admin)
                amount=total_amount,  # Assuming seat has a price attribute
                transaction_date=local_time,
                status="completed"  # Set payment status
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

# def film_maker_view_mssges(request):
#     # Get all chat messages
#     chats = chat.objects.all()

#     # Extract unique login_ids from 'fromid' and 'toid' fields
#     theater_owner_login_ids = set(chats.values_list('fromid', flat=True)) | set(chats.values_list('toid', flat=True))

#     # Fetch TheaterOwner details where login_id matches 'fromid' or 'toid'
#     theater_owners = TheaterOwner.objects.filter(login__login_id__in=theater_owner_login_ids).values(
#         'owner_id', 'name', 'email', 'phone', 'profile_image', 'login__login_id'
#     )

#     return render(request, 'film_maker_view_mssges.html', {'theater_owners': theater_owners})


def film_maker_view_mssges(request):
    theater_owners=TheaterOwner.objects.all()
    return render(request,'film_maker_view_mssges.html', {'theater_owners': theater_owners})


def film_maker_chat_owners(request,id):
    owner_id=id
    request.session["owner_id"]=owner_id
    from_id=request.session['login_id']
    print("hiiiiiiiiii",owner_id,from_id)
    return render(request,'film_maker_chat_owners.html',{"toid":id})

from django.db.models import Q

def film_maker_view_producermsg(request):
    print("###")
    current_theatre_id = request.session['login_id']
    print("&&&&&&&&&")
    a=[]
    chat_messages = chat.objects.filter(
        Q(fromid=current_theatre_id, toid=request.session['owner_id']) | Q(fromid=request.session['owner_id'], toid=current_theatre_id)
    )
    for i in chat_messages:
        a.append({"chat_id":i.chatid,"from_id":i.fromid,"message":i.message,"date_time":i.date})
    p=TheaterOwner.objects.get(login_id=request.session["owner_id"])
    print(chat_messages,p.name)
    prof = p.license_photo
    print(prof,"YYYYYYYYYYYYYYYYY")
    first_name=p.name+" "
    print(a)
    # return JsonResponse({'data':a,'first_name':first_name,'photo':"/static/image/chat_profile.jpg"})
    return JsonResponse({'data':a,'first_name':first_name,'photo':f"/static/image/{prof}"})


def film_maker_view_films(request):
    films=film.objects.filter(filmmaker_id=request.session['fm_id'])
    if request.method=='POST':
        film_name=request.POST['film']
        details=request.POST['deat']
        date=request.POST['redate']
        # film_maker_id=request.POST['film_maker_id']

        # fm_id = Filmmaker.objects.get(filmmaker_id=film_maker_id)

        photo=request.FILES['photo']




        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)

        # try:
        flm=film(film_name=film_name,deatils=details,photo=image,date=date,filmmaker_id=request.session['fm_id'])
        flm.save()
        return HttpResponse("<script>alert('Film Added Successfully');window.location='/film_maker_view_films';</script>")

        # except:
        #     return HttpResponse("<script>alert('FAILED');window.location='/admin_manage_films';</script>")
    return render(request,'film_maker_view_films.html',{'films':films})



from django.shortcuts import render
# from .models import BookTheaters

def film_maker_view_theater_book_status(request):
    filmmaker_id = request.session.get('fm_id')  # Fetch logged-in filmmaker ID
    bookings = BookTheaters.objects.filter(fimmaker_id=filmmaker_id).select_related('film', 'theater__owner')

    return render(request, "film_maker_view_theater_book_status.html", {'bookings': bookings})

def make_payment_for_therate_booking(request,theater_id):
    bookings = BookTheaters.objects.get(Booktheater_id=theater_id)

    if request.method == 'POST':
        bookings.status = "Paid"
        bookings.save()
        return HttpResponse("<script>alert('Pay  Successfully');window.location='/filmaker_home';</script>")

  
    return render(request, "make_payment_for_therate_booking.html",)



def film_maker_add_promotion_materials(request, film_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        release_date = request.POST['release_date']
        poster = request.FILES['poster']  # File upload handling

        # Save file to media storage
        fs = FileSystemStorage()
        poster_path = fs.save(poster.name, poster)

        # Get the associated film instance
        film_instance = film.objects.get(filmid=film_id)

        # Save promo material
        promo = PromoMaterial(
            film=film_instance,
            title=title,
            description=description,
            release_date=release_date,
            poster=poster_path,
            status = "Pending"
        )
        promo.save()

        return HttpResponse("<script>alert('Promotion Material Added Successfully');window.location='/film_maker_view_films';</script>".format(film_id))
    

    # Fetch all promotion materials for this film
    promo_materials = PromoMaterial.objects.filter(film_id=film_id)

    return render(request, 'film_maker_add_promotion_materials.html', {
        'film_id': film_id,
        'promo_materials': promo_materials
    })


def delete_promo_materials(request, promo_id):
    promo = PromoMaterial.objects.get(promo_id=promo_id)

    film_id = promo.film.filmid  # Get the associated film ID before deleting
    promo.delete()

    return HttpResponse("<script>alert('Promotion Material Deleted Successfully');window.location='/film_maker_view_films';</script>".format(film_id))



import datetime


# def film_maker_view_theaters(request,film_id):
#     return render(request,"film_maker_view_theaters.html")


def theatre_insert_theatrechat(request, msg):
    try:
        # Verify session variables exist
        from_id = request.session.get('login_id')
        to_id = request.session.get('owner_id')

        print("from_id",from_id)
        print("to_id",to_id)
        
        # Add error handling
        if not from_id or not to_id:
            return JsonResponse({'status': 'error', 'message': 'Missing session variables'})
        
        # Create and save chat object
        new_chat = chat(
            fromid=from_id, 
            toid=to_id, 
            message=msg, 
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        new_chat.save()
        
        return JsonResponse({'status': "ok"})
    
    except Exception as e:
        # Log the error and return an error response
        print(f"Error inserting chat message: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


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

# from django.shortcuts import render, redirect
# from django.db.models import Q
# from django.utils.timezone import now
# # from .models import Chat, TheaterOwner

# def film_maker_chat_owners(request, login_id):
#     sender_id = request.session.get('login_id')  # Filmmaker's login ID
#     receiver_id = login_id  # Theater owner's login ID
    
#     # Fetch chat messages (both sent & received)
#     messages = chat.objects.filter(
#         Q(fromid=sender_id, toid=receiver_id) | Q(fromid=receiver_id, toid=sender_id)
#     ).order_by('date')  # Order messages by date (ensure it's the correct field for ordering)

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




from django.shortcuts import render, get_object_or_404

def conter_manager_view_promo(request, film_id): 
    # Fetch the film object
    film_instance = get_object_or_404(film, filmid=film_id)
    
    # Get all promo materials related to the film
    promo_materials = PromoMaterial.objects.filter(film=film_instance)

    return render(request, "conter_manager_view_promo.html", {
        'film': film_instance,
        'promo_materials': promo_materials
    })



def accept_promo_material(request, promo_id):
    promo = get_object_or_404(PromoMaterial, promo_id=promo_id)
    promo.status = "Accepted"
    promo.save()
    return HttpResponse("<script>alert('Promotion Material Accepted Successfully');window.location='/conter_manager_view_films_to_make_campaign';</script>") # Redirect back to the promo list

def reject_promo_material(request, promo_id):
    promo = get_object_or_404(PromoMaterial, promo_id=promo_id)
    promo.status = "Rejected"
    promo.save()
    return HttpResponse("<script>alert('Promotion Material Rejected Successfully');window.location='/conter_manager_view_films_to_make_campaign';</script>")



####################User App#######################
def user_app_login(request):
    data = []
    username = request.GET.get('username')
    password = request.GET.get('password')

    try:
        print(f"Received username: {username}, password: {password}")

        # Fetch all records from the login table
        queryset = Login.objects.filter(username=username, password=password)

        print(f"Queryset count: {queryset.count()}")

        login_data = queryset.values('login_id', 'usertype').first()
        print(f"Fetched login data: {login_data}")

        if not login_data:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})

        if login_data['usertype'] == 'user':
            queryset2 = Audience.objects.filter(login_id=login_data['login_id']).values('audience_id')
            data = [{"user_id": u['audience_id'], "usertype": login_data['usertype'], "login_id": login_data['login_id']} for u in queryset2]

        status = "success" if data else "error"

    except Exception as e:
        status = "error"
        print(f"Error: {e}")

    response = {'status': status, 'user': data}
    print(response,"*********************")
    
    return JsonResponse(response)


def user_app_signup(request):
    data=[]
    name=request.GET.get('name')
    phone=request.GET.get('phone')
    email=request.GET.get('email')
    preferences=request.GET.get('preferences')
    username=request.GET.get('username')
    password=request.GET.get('password')

    try:
        x=Login(username=username,password=password,usertype='user')
        x.save()

        a=Audience(name=name,phone=phone,email=email,preferences=preferences,login=x)
        a.save()
        status="success"

    except Exception as e:
        status="error"

    response={
        'status':status
    }

    return JsonResponse(response)


from django.db.models import Avg
from django.http import JsonResponse
import traceback

def user_app_view_films(request):
    data = []
    try:
        films = film.objects.all()
        for f in films:
            # Calculate average rating (Convert to float, handle missing ratings)
            avg_rating = Review.objects.filter(film=f).aggregate(avg_rating=Avg('rating'))['avg_rating']
            avg_rating = round(float(avg_rating), 1) if avg_rating is not None else 0.0

            data.append({
                'filmid': f.filmid,
                'film_name': f.film_name,
                'filmmaker': f.filmmaker_id if f.filmmaker else None,  
                'details': f.deatils,  
                'photo': f.photo,  
                'date': f.date,
                'average_rating': avg_rating  # New field added
            })
        status = "success"
    except Exception as e:
        print("Error occurred in user_app_view_films:")
        traceback.print_exc()
        status = "error"

    response = {
        'status': status,
        'films': data,
        'method': 'films'
    }

    print(response, "FILM DATA")
    return JsonResponse(response)


from django.db.models import Q, Avg
from django.http import JsonResponse
import traceback

def user_app_search_films(request):
    search = request.GET.get('q', '').strip()  # Get search query, handle empty input
    data = []

    try:
        # Filter films where the search text is in the film name (case-insensitive)
        films = film.objects.filter(Q(film_name__icontains=search))

        for f in films:
            # Calculate average rating (Convert to float, handle missing ratings)
            avg_rating = Review.objects.filter(film=f).aggregate(avg_rating=Avg('rating'))['avg_rating']
            avg_rating = round(float(avg_rating), 1) if avg_rating is not None else 0.0

            data.append({
                'filmid': f.filmid,
                'film_name': f.film_name,
                'filmmaker': f.filmmaker_id if f.filmmaker else None,  
                'details': f.deatils,  
                'photo': f.photo,  
                'date': f.date,
                'average_rating': avg_rating  # New field added
            })

        status = "success" if data else "failed"

    except Exception as e:
        print("Error occurred in user_app_search_films:")
        traceback.print_exc()
        status = "error"

    response = {
        'status': status,
        'films': data,
        'method': 'films'
    }

    print(response, "SEARCH FILM DATA")
    return JsonResponse(response)


def user_app_send_complaint(request):
    title = request.GET.get('title')
    description = request.GET.get('description')
    login_id = request.GET.get('login_id')


    try:
        res = complaint(
            complaint=title,
            reply='pending',
            date=date.today(),
            senderid=Login.objects.get(login_id=login_id)        )
        res.save()
        status = "success"  

    except Exception as e:
        status = "error"
        print(f"Error: {e}")

    response = {
        'status': status,
        'method': 'send'
    }

    return JsonResponse(response)


def user_view_app_complaint(request):
    login_id = request.GET.get('login_id')
    data=[]

    try:
        res = complaint.objects.filter(senderid=Login.objects.get(login_id=login_id))
        for i in res:
            data.append({'complaint_id':i.complaintid,'title':i.complaint,'reply':i.reply,'date':i.date})
        status = "success"

    except Exception as e:
        status = "error"
        print(f"Error: {e}")

    response = {
        'status': status,
        'view': data,
        'method': 'display'
    }
    print(response,"^^^^^^^^^^^")

    return JsonResponse(response)


from django.shortcuts import render
from django.http import JsonResponse
from collections import defaultdict
# from .models import ScreeningSlot, Theater

def user_app_view_theaters(request):
    data = []
    film_id = request.GET.get('film_id')
    date = request.GET.get('date')

    if not film_id or not date:
        return JsonResponse({'error': 'film_id and date are required'}, status=400)

    # Fetch screening slots for the given film_id and date
    slots = ScreeningSlot.objects.filter(film_id=film_id, date=date).select_related('theater')

    # Dictionary to group slots by theater
    theater_slots = defaultdict(list)

    for slot in slots:
        theater_slots[slot.theater].append({
            'slot_id': slot.slot_id,
            'start_time': slot.start_time.strftime('%H:%M:%S'),
            'status': slot.status,
            'film_id': slot.film_id  # Include film_id in slot details
        })

    # Construct response
    for theater, slot_details in theater_slots.items():
        data.append({
            'theater_id': theater.theater_id,
            'name': theater.name,
            'location': theater.location,
            'capacity': theater.capacity,
            'contact_email': theater.contact_email,
            'contact_phone': theater.contact_phone,
            'slots': slot_details  # Now includes film_id
        })

    response = {
        'status': 'success',
        'theaters': data
    }

    print(response,"MMMMMMMMMMMMMMM")

    return JsonResponse(response)

from django.http import JsonResponse
# from .models import TheaterSeat

def user_app_view_seats_to_book(request):
    slot_id = request.GET.get('slot_id')

    if not slot_id:
        response={"status": "failed"}
        return JsonResponse(response)

    try:
        seats = TheaterSeat.objects.filter(slot_id=slot_id).values(
            'seat_id', 'seat_number', 'seat_type', 'status', 'slot_id'
        )
        response={"status": "success", "seats": list(seats)}
        print(response,"<<<<<<<<<<<<<<<<<<<<<<<<")
        return JsonResponse(response)
    
    except Exception as e:
        response={"status": "failed"}
        return JsonResponse(response)

# from django.http import JsonResponse
# from django.utils.timezone import now

# def user_app_seat_booking(request):
#     seat_ids = request.GET.get('seat_ids')  # Get seat_ids as a string
#     user_id = request.GET.get('user_id')
#     slot_id = request.GET.get('slot_id')
#     theater_id = request.GET.get('theater_id')
#     film_id = request.GET.get('film_id')

#     if not seat_ids or not user_id or not slot_id or not film_id:
#         return JsonResponse({"status": "failed", "message": "Missing required parameters"})

#     # Convert seat_ids string to a list
#     seat_id_list = seat_ids.split(',')

#     # Fetch related objects
#     try:
#         slot = ScreeningSlot.objects.get(slot_id=slot_id)
#         filmObj = film.objects.get(filmid=film_id)
#         audience = Audience.objects.get(audience_id=user_id)  # Assuming user_id belongs to Audience
#     except (ScreeningSlot.DoesNotExist, film.DoesNotExist, Audience.DoesNotExist):
#         return JsonResponse({"status": "failed", "message": "Invalid slot, film, or user ID"})

#     # Insert records into SeatBooking model
#     for seat_id in seat_id_list:
#         try:
#             seat = TheaterSeat.objects.get(seat_id=seat_id)
#             SeatBooking.objects.create(
#                 slot=slot,
#                 seat=seat,
#                 audience=audience,
#                 filmmaker=None,  # If filmmaker is not involved, set to None
#                 payment_status="paid",  # Adjust based on logic
#                 film=filmObj,
#                 booking_date=now()
#             )
#         except TheaterSeat.DoesNotExist:
#             return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} does not exist"})

#     return JsonResponse({"status": "success", "seat_ids": seat_id_list})


# from django.http import JsonResponse
# from django.utils.timezone import now
# from django.db import transaction

# def user_app_seat_booking(request):
#     seat_ids = request.GET.get('seat_ids')  # Get seat_ids as a string
#     user_id = request.GET.get('user_id')
#     slot_id = request.GET.get('slot_id')
#     theater_id = request.GET.get('theater_id')
#     film_id = request.GET.get('film_id')
#     tot_price = request.GET.get('tot_price')

#     if not seat_ids or not user_id or not slot_id or not film_id:
#         return JsonResponse({"status": "failed", "message": "Missing required parameters"})

#     # Convert seat_ids string to a list
#     seat_id_list = seat_ids.split(',')

#     # Fetch related objects
#     try:
#         slot = ScreeningSlot.objects.get(slot_id=slot_id)
#         filmObj = film.objects.get(filmid=film_id)
#         audience = Audience.objects.get(audience_id=user_id)  # Assuming user_id belongs to Audience
#     except (ScreeningSlot.DoesNotExist, film.DoesNotExist, Audience.DoesNotExist):
#         return JsonResponse({"status": "failed", "message": "Invalid slot, film, or user ID"})

#     # Use transaction to ensure atomic operations
#     with transaction.atomic():
#         for seat_id in seat_id_list:
#             try:
#                 seat = TheaterSeat.objects.get(seat_id=seat_id, slot=slot)
#                 if seat.status == "booked":
#                     return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} is already booked"})
                
#                 # Insert into SeatBooking
#                 SeatBooking.objects.create(
#                     slot=slot,
#                     seat=seat,
#                     audience=audience,
#                     filmmaker=None,  # If filmmaker is not involved, set to None
#                     payment_status="paid",  # Adjust based on logic
#                     film=filmObj,
#                     booking_date=now()
#                 )
                
#                 # Update seat status to booked
#                 seat.status = "booked"
#                 seat.save()
#             except TheaterSeat.DoesNotExist:
#                 return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} does not exist or is not available for the given slot"})

#     return JsonResponse({"status": "success", "seat_ids": seat_id_list})




# from django.http import JsonResponse
# from django.utils.timezone import now
# from django.db import transaction

# def user_app_seat_booking(request):
#     seat_ids = request.GET.get('seat_ids')  # Get seat_ids as a string
#     user_id = request.GET.get('user_id')
#     slot_id = request.GET.get('slot_id')
#     theater_id = request.GET.get('theater_id')
#     film_id = request.GET.get('film_id')
#     tot_price = request.GET.get('tot_price')

#     if not seat_ids or not user_id or not slot_id or not film_id or not theater_id or not tot_price:
#         return JsonResponse({"status": "failed", "message": "Missing required parameters"})

#     # Convert seat_ids string to a list
#     seat_id_list = seat_ids.split(',')

#     # Fetch related objects
#     try:
#         slot = ScreeningSlot.objects.get(slot_id=slot_id)
#         filmObj = film.objects.get(filmid=film_id)
#         audience = Audience.objects.get(audience_id=user_id)  # Assuming user_id belongs to Audience
#         # payer = Login.objects.get(id=user_id)  # Payer (User)
#         # receiver = Login.objects.get(id=theater_id)  # Receiver (Theater)
#     except (ScreeningSlot.DoesNotExist, film.DoesNotExist, Audience.DoesNotExist, Login.DoesNotExist):
#         return JsonResponse({"status": "failed", "message": "Invalid slot, film, user, or theater ID"})

#     # Use transaction to ensure atomic operations
#     with transaction.atomic():
#         bookings = []  # Store booked seats to associate with payment
#         for seat_id in seat_id_list:
#             try:
#                 seat = TheaterSeat.objects.get(seat_id=seat_id, slot=slot)
#                 if seat.status == "booked":
#                     return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} is already booked"})

#                 # Insert into SeatBooking
#                 booking = SeatBooking.objects.create(
#                     slot=slot,
#                     seat=seat,
#                     audience=audience,
#                     filmmaker=None,  # If filmmaker is not involved, set to None
#                     payment_status="paid",  # Adjust based on logic
#                     film=filmObj,
#                     booking_date=now()
#                 )
#                 bookings.append(booking)

#                 # Update seat status to booked
#                 seat.status = "booked"
#                 seat.save()
#             except TheaterSeat.DoesNotExist:
#                 return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} does not exist or is not available for the given slot"})

#         # Insert into Payment model
#         Payment.objects.create(
#             booking=bookings[0],  # Linking to the first booking (since payment covers multiple seats)
#             payer_id=user_id,
#             receiver_id=theater_id,
#             amount=tot_price,
#             transaction_date=now(),
#             status="completed"
#         )

#     return JsonResponse({"status": "success", "seat_ids": seat_id_list})



from django.http import JsonResponse
from django.utils.timezone import now
from django.db import transaction

def user_app_seat_booking(request):
    seat_ids = request.GET.get('seat_ids')  # Get seat_ids as a string
    user_id = request.GET.get('user_id')
    slot_id = request.GET.get('slot_id')
    theater_id = request.GET.get('theater_id')
    film_id = request.GET.get('film_id')
    tot_price = request.GET.get('tot_price')

    if not seat_ids or not user_id or not slot_id or not film_id or not theater_id or not tot_price:
        return JsonResponse({"status": "failed", "message": "Missing required parameters"})

    # Convert seat_ids string to a list
    seat_id_list = seat_ids.split(',')

    try:
        slot = ScreeningSlot.objects.get(slot_id=slot_id)
        filmObj = film.objects.get(filmid=film_id)
        audience = Audience.objects.get(audience_id=user_id)
    except (ScreeningSlot.DoesNotExist, film.DoesNotExist, Audience.DoesNotExist):
        return JsonResponse({"status": "failed", "message": "Invalid slot, film, or user ID"})

    try:
        total_amount = float(tot_price)  # Convert total price to float
        seat_count = len(seat_id_list)
        per_seat_price = total_amount / seat_count  # Calculate price per seat
    except ValueError:
        return JsonResponse({"status": "failed", "message": "Invalid total price value"})

    with transaction.atomic():
        bookings = []  
        for seat_id in seat_id_list:
            try:
                seat = TheaterSeat.objects.get(seat_id=seat_id, slot=slot)
                if seat.status == "booked":
                    return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} is already booked"})

                booking = SeatBooking.objects.create(
                    slot=slot,
                    seat=seat,
                    audience=audience,
                    filmmaker=None,
                    payment_status="paid",
                    film=filmObj,
                    booking_date=now()
                )
                bookings.append(booking)

                # Update seat status
                seat.status = "booked"
                seat.save()
            except TheaterSeat.DoesNotExist:
                return JsonResponse({"status": "failed", "message": f"Seat ID {seat_id} does not exist or is not available for the given slot"})

        # Insert separate Payment records for each SeatBooking
        for booking in bookings:
            Payment.objects.create(
                booking=booking,
                payer_id=user_id,
                receiver_id=theater_id,
                amount=per_seat_price,  # Assign per-seat price to each payment record
                transaction_date=now(),
                status="completed"
            )

    return JsonResponse({"status": "success", "seat_ids": seat_id_list})



from django.http import JsonResponse

def user_view_app_nots(request):
    try:
        # Fetch all notifications
        notifications = notification.objects.all().values(
            'notification_id', 'notifications', 'title', 'date'
        )

        response = {
            "status": "success",
            "notifications": list(notifications)
        }

        print(response,"MMMMMMMMM")

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"status": "failed", "message": str(e)})

from django.http import JsonResponse
# from .models import SeatBooking, Payment, TheaterSeat, ScreeningSlot, Film, Theater

def user_view_app_bookings(request):
    try:
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({"status": "failed", "message": "User ID is required"})

        # Fetch all bookings by the user
        bookings = SeatBooking.objects.filter(audience_id=user_id).select_related(
            'slot', 'seat', 'film', 'slot__theater'
        )

        booking_list = []

        for booking in bookings:
            # Fetch payment details
            payment = Payment.objects.filter(booking=booking).first()
            payment_status = payment.status if payment else "Not Paid"
            amount = payment.amount if payment else 0.00

            booking_list.append({
                "booking_id": booking.booking_id,
                "booking_date": booking.booking_date,
                "payment_status": payment_status,
                "amount_paid": amount,
                "theater_name": booking.slot.theater.name,
                "theater_location": booking.slot.theater.location,
                "seat_number": booking.seat.seat_number,
                "seat_type": booking.seat.seat_type,
                "slot_start_time": booking.slot.start_time,
                "slot_end_time": booking.slot.end_time,
                "slot_date": booking.slot.date,
                "film_name": booking.film.film_name if booking.film else "N/A",
                "image": booking.film.photo if booking.film else ""
            })

        response = {
            "status": "success",
            "bookings": booking_list,
            'method':'bookings'
        }

        print(response,"MMMMMMMMMm")

        return JsonResponse(response, safe=False)

    except Exception as e:
        return JsonResponse({"status": "failed", "message": str(e)})

from django.http import JsonResponse
from django.utils.timezone import now

def user_app_add_rating(request):
    try:
        user = Audience.objects.get(audience_id=request.GET.get('user_id'))
        movie = film.objects.get(filmid=request.GET.get('film_id'))

        rating_obj = Review.objects.create(
            audience=user,
            film=movie,
            rating=request.GET.get('rating'),
            review_text=request.GET.get('review'),
            review_date=now()
        )

        return JsonResponse({"status": "success"})

    except Audience.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "Invalid user ID"})
    except film.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "Invalid film ID"})
    except Exception as e:
        return JsonResponse({"status": "failed", "message": str(e)})
    



from django.http import JsonResponse
from django.db.models import Count, Avg
import traceback

def user_app_view_film_recommendations(request):
    data = []
    try:
        # Get films ranked by number of bookings
        films = film.objects.annotate(
            booking_count=Count('screeningslot__seatbooking')
        ).order_by('-booking_count')

        for f in films:
            # Calculate average rating (Convert to float, handle missing ratings)
            avg_rating = Review.objects.filter(film=f).aggregate(avg_rating=Avg('rating'))['avg_rating']
            avg_rating = round(float(avg_rating), 1) if avg_rating is not None else 0.0

            data.append({
                'filmid': f.filmid,
                'film_name': f.film_name,
                'filmmaker': f.filmmaker_id if f.filmmaker else None,  
                'details': f.deatils,  
                'photo': f.photo,  
                'date': f.date,
                'average_rating': avg_rating,  # New field added
                'booking_count': f.booking_count  # New field added
            })

        status = "success"
    except Exception as e:
        print("Error occurred in user_app_view_film_recommendations:")
        traceback.print_exc()
        status = "error"

    response = {
        'status': status,
        'films': data,
        'method': 'film_recommendations'
    }

    print(response, "FILM RECOMMENDATION DATA")
    return JsonResponse(response)