import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bridgeApp.models import *
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

# Create your views here.



def theatre_owner_registration(request):

    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['mail']
        phone=request.POST['phone']
        photo=request.FILES['photo']
        username=request.POST['uname']
        password=request.POST['pass']


        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)

        try:
            lg=Login.objects.get(username=username)
            if lg:
                return HttpResponse("<script>alert('UserName Already Exist');window.location='/theatre_owner_registration';</script>")
        except:
            lg=Login(username=username,password=password,usertype='pending')
            lg.save()

            th=TheaterOwner(name=name,email=email,phone=phone,license_photo=image,login_id=lg.pk)
            th.save()

            return HttpResponse("<script>alert('Added Successfully');window.location='/theatre_owner_registration';</script>")

    return render(request,'theatre_owner_registration.html')


def theatre_home(request):
    return render(request,'theatre_home.html')

def theatre_view_profile(request):
    th=TheaterOwner.objects.get(login_id=request.session['login_id'])
    return render(request,'theatre_view_profile.html',{'th':th})

def thearter_owner_update_profile(request,lid):
    thup=TheaterOwner.objects.get(login_id=lid)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['mail']
        phone=request.POST['phone']
        photo=request.FILES['photo']

        thup.name=name
        thup.email=email
        thup.phone=phone
        thup.license_photo=photo
        thup.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/theatre_view_profile';</script>")

    return render(request,'theatre_view_profile.html',{'thup':thup})

def theatre_registration(request):

    res=TheaterOwner.objects.get(login_id=request.session['login_id'])
    print(res.owner_id)

    th= Theater.objects.filter(owner_id=res.owner_id)

    if request.method=='POST':
        name=request.POST['tname']
        email=request.POST['mail']
        location=request.POST['loca']
        capacity=request.POST['cap']
        phone=request.POST['phone']

        res=TheaterOwner.objects.get(login_id=request.session['login_id'])
        print(res.owner_id)

        th=Theater(name=name,contact_email=email,location=location,capacity=capacity,contact_phone=phone,owner_id=res.owner_id)
        th.save()

        return HttpResponse("<script>alert('Added Successfully');window.location='/thearte_registration';</script>")

    return render(request,'theatre_registration.html',{'th':th})



def theatre_view_others_theartes(request):

    res=TheaterOwner.objects.get(login_id=request.session['login_id'])
    print(res.owner_id)

    th= Theater.objects.exclude(owner_id=res.owner_id)

    return render(request,'theatre_view_others_theartes.html',{'th':th})


def theatre_manage_seats(request,id):
    st=TheaterSeat.objects.filter(theater_id=id)
    if request.method=='POST':
        seat_number=request.POST['snum']
        seat_type=request.POST['stype']

        ts=TheaterSeat(theater_id=id,seat_number=seat_number,seat_type=seat_type,status='pending')
        ts.save()

        return HttpResponse("<script>alert('Added Successfully');window.location='/thearte_registration';</script>")
    return render(request,'theatre_manage_seats.html',{'st':st})


def theatre_manage_slots(request,id):
    flm=film.objects.all()
    st=ScreeningSlot.objects.filter(theater_id=id)

    if request.method=='POST':
        start_time=request.POST['stime']
        end_time=request.POST['endtime']
        date=request.POST['date']
        flm_id=request.POST['flm']

        ts=ScreeningSlot(theater_id=id,film_id=flm_id,start_time=start_time,end_time=end_time,date=date,status='pending')
        ts.save()

        return HttpResponse("<script>alert('Added Successfully');window.location='/thearte_registration';</script>")
    return render(request,'theatre_manage_slots.html',{'flm':flm,'st':st})

def theatre_update_slots(request,id):
    flm=film.objects.all()
    upst=ScreeningSlot.objects.get(slot_id=id)

    if request.method=='POST':
        start_time=request.POST['stime']
        end_time=request.POST['endtime']
        date=request.POST['date']
        flm_id=request.POST['flm']

        upst.start_time=start_time
        upst.end_time=end_time
        upst.date=date
        upst.film_id=flm_id
        upst.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/thearte_registration';</script>")

    return render(request,'theatre_manage_slots.html',{'flm':flm,'upst':upst})
    
    

def theatre_delete_slots(request,id):
    upst=ScreeningSlot.objects.get(slot_id=id)
    upst.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/thearte_registration';</script>")


def thearte_view_booking(request,id):
    bks=SeatBooking.objects.filter(slot_id=id)
    return render(request,'theatre_view_booking.html',{'bks':bks})


def theatre_view_payment_details(request,id):
    pmt=Payment.objects.filter(booking_id=id)
    return render(request,'theatre_view_payment_details.html',{'pmt':pmt})


def theatre_view_producers(request):
    pro=Filmmaker.objects.all()
    return render(request,'theatre_view_producers.html',{'pro':pro})



def theatre_chat(request,id):
    owner_id=id
    request.session["owner_id"]=owner_id
    from_id=request.session['login_id']
    print("hiiiiiiiiii",owner_id,from_id)
    return render(request,'theatre_chat_producers.html',{"toid":id})



def theatre_view_producermsg(request):
    print("###")
    current_theatre_id = request.session['login_id']
    print("&&&&&&&&&")
    a=[]
    chat_messages = chat.objects.filter(
        Q(fromid=current_theatre_id, toid=request.session['owner_id']) | Q(fromid=request.session['owner_id'], toid=current_theatre_id)
    )
    for i in chat_messages:
        a.append({"chat_id":i.chatid,"from_id":i.fromid,"message":i.message,"date_time":i.date})
    p=Filmmaker.objects.get(login_id=request.session["owner_id"])
    print(chat_messages,p.name)
    first_name=p.name+" "
    print(a)
    return JsonResponse({'data':a,'first_name':first_name,'photo':"/static/image/chat_profile.jpg"})


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