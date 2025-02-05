from django.db import models

# Create your models here.

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    usertype = models.CharField(max_length=50)

class Filmmaker(models.Model):
    filmmaker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    login = models.ForeignKey('Login', on_delete=models.CASCADE)

class TheaterOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images/')
    login = models.ForeignKey('Login', on_delete=models.CASCADE)

class Theater(models.Model):
    theater_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(TheaterOwner, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)



class ScreeningSlot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)
    film = models.ForeignKey('Film', null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=20)

class TheaterSeat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)
    slot = models.ForeignKey(ScreeningSlot, on_delete=models.CASCADE, default=None)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('SeatBooking', null=True, blank=True, on_delete=models.CASCADE)
    payer = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='payer')
    receiver = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    status = models.CharField(max_length=20)

class Audience(models.Model):
    audience_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    preferences = models.CharField(max_length=225)
    login = models.ForeignKey('Login', on_delete=models.CASCADE)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    audience = models.ForeignKey('Audience', on_delete=models.CASCADE)
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField()

class SeatBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey('ScreeningSlot', on_delete=models.CASCADE)
    seat = models.ForeignKey('TheaterSeat', on_delete=models.CASCADE)
    audience = models.ForeignKey('Audience', null=True, blank=True, on_delete=models.CASCADE)
    filmmaker = models.ForeignKey('Filmmaker', null=True, blank=True, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20)
    booking_date = models.DateTimeField()

class MarketingCampaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    filmmaker = models.ForeignKey('Filmmaker', on_delete=models.CASCADE)
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    manager = models.ForeignKey('ContentManager', on_delete=models.CASCADE)

class Ad(models.Model):
    ad_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey('MarketingCampaign', on_delete=models.CASCADE)
    target_audience = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    manager = models.ForeignKey('ContentManager', on_delete=models.CASCADE)



class ContentManager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=255)
    login = models.ForeignKey('Login', on_delete=models.CASCADE)





class complaint(models.Model):
    complaintid=models.AutoField(primary_key=True)
    senderid=models.ForeignKey(Login,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=225)
    reply=models.CharField(max_length=225)
    date=models.CharField(max_length=225)


class film(models.Model):
    filmid=models.AutoField(primary_key=True)
    film_name=models.CharField(max_length=225)
    deatils=models.CharField(max_length=225)
    photo=models.FileField()
    date=models.CharField(max_length=225)


class notification(models.Model):
    notification_id=models.AutoField(primary_key=True)
    notifications=models.CharField(max_length=225)
    title=models.CharField(max_length=225)
    date=models.CharField(max_length=225)


class chat(models.Model):
    chatid=models.AutoField(primary_key=True)
    fromid=models.CharField(max_length=225)
    toid=models.CharField(max_length=225)
    date=models.CharField(max_length=225)
    message=models.CharField(max_length=225)
