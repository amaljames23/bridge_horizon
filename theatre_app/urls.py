from django.urls import path
from . import views

urlpatterns = [

    path('theatre_home',views.theatre_home,name='theatre_home'),
    path('thearte_registration',views.theatre_registration,name='thearte_registration'),





]