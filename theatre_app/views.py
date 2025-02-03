from django.http import HttpResponse
from django.shortcuts import render
from bridgeApp.models import *


# Create your views here.


def theatre_home(request):
    return render(request,'theatre_home.html')




def theatre_registration(request):

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

        return HttpResponse("<script>alert(' Added Successfully');window.location='/thearte_registration';</script>")


    return render(request,'theatre_registration.html')


