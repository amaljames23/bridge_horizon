from django.http import HttpResponse
from django.shortcuts import render
from . models import *
from django.core.files.storage import FileSystemStorage

# Create your views here.



def home(request):
    return render(request,'home.html')

def login_form(request):

    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['pass']   

        try:
            lg=Login.objects.get(username=username,password=password)
            request.session['login_id']=lg.pk

            if lg.usertype=='admin':
                return HttpResponse("<script>alert('Login Successfully');window.location='/adminhome';</script>")
            if lg.usertype=='owner':
                return HttpResponse("<script>alert('Login Successfully');window.location='/theatre_home';</script>")

        except:
            return HttpResponse("<script>alert('Invalid Username Or Password');window.location='/login';</script>")

    return render(request,'login.html')


def theatre_owner_registration(request):
    return render(request,'theatre_owner_registration.html')



########################Admin####################################


def adminhome(request):
    return render(request,'adminhome.html')

def admin_manage_users(request):

    usr=Audience.objects.all()

    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['mail']
        phone=request.POST['phone']
        Preferences=request.POST['per']
        username=request.POST['uname']
        password=request.POST['pass']

        try:
            lg=Login.objects.get(username=username,password=password)
            if lg:
                return HttpResponse("<script>alert('UserName Already Exist');window.location='/admin_manage_users';</script>")
        except:
            lg=Login(username=username,password=password,usertype='user')
            lg.save()

            aud=Audience(name=name,email=email,phone=phone,preferences=Preferences,login_id=lg.pk)
            aud.save()
            return HttpResponse("<script>alert('User Added Successfully');window.location='/admin_manage_users';</script>")

    return render(request,'admin_manage_users.html',{'usr':usr})

def delete_user(request,aid):
    aud=Audience.objects.get(audience_id=aid)
    aud.delete()
    return HttpResponse("<script>alert(' Deleted Successfully');window.location='/admin_manage_users';</script>")

def admin_view_compalints(request):
    comp=complaint.objects.all()
    return render(request,'admin_view_compalints.html',{'comp':comp})


def admin_send_reply(request,cid):
    comp=complaint.objects.get(complaintid=cid)

    if request.method=='POST':
        reply=request.POST['reply']
        comp.reply=reply
        comp.save()
        return HttpResponse("<script>alert('Reply Send Successfully');window.location='/admin_view_compalints';</script>")

    return render(request,'admin_send_reply.html')


def admin_manage_films(request):
    films=film.objects.all()

    print(films,"////////////////////////////")

    if request.method=='POST':
        film_name=request.POST['film']
        details=request.POST['deat']
        date=request.POST['redate']
        photo=request.FILES['photo']


        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)

        try:
            flm=film(film_name=film_name,deatils=details,photo=image,date=date)
            flm.save()
            return HttpResponse("<script>alert('Film Added Successfully');window.location='/admin_manage_films';</script>")

        except:
            return HttpResponse("<script>alert('FAILED');window.location='/admin_manage_films';</script>")
    
    return render(request,'admin_manage_films.html',{'films':films})


def admin_delete_films(request,id):
    fimdet=film.objects.get(filmid=id)
    fimdet.delete()
    return HttpResponse("<script>alert(' Deleted Successfully');window.location='/admin_manage_films';</script>")


def admin_update_films(request,id):
    fimupd=film.objects.get(filmid=id)

    if request.method=='POST':
        film_name=request.POST['film']
        details=request.POST['deat']
        date=request.POST['redate']
        photo=request.FILES['photo']

        fs= FileSystemStorage()
        image=fs.save(photo.name,photo)

        fimupd.film_name=film_name
        fimupd.deatils=details
        fimupd.date=date
        fimupd.photo=image
        fimupd.save()
        return HttpResponse("<script>alert('Film Updated Successfully');window.location='/admin_manage_films';</script>")


    return render(request,'admin_manage_films.html',{'fimupd':fimupd})



def admin_view_Review(request):
    revv=Review.objects.all()
    return render(request,'admin_view_Review.html',{'revv':revv})
    

def admin_send_notification(request):

    return render(request,'admin_send_notification.html')