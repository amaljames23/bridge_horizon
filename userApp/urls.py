from django.urls import path
from . import views

urlpatterns = [
    path('user_home',views.user_home,name='user_home'),
    path('user_reg',views.user_reg,name='user_reg'),
    path('user_view_nots',views.user_view_nots,name='user_view_nots'),
    path('user_send_complaints',views.user_send_complaints,name='user_send_complaints'),
    path('user_view_theaters',views.user_view_theaters,name='user_view_theaters'),
    path('user_book_seats/<theater_id>/<screening_slot_id>',views.user_book_seats,name='user_book_seats'),
    path('user_seat_confirm/', views.user_seat_confirm, name='user_seat_confirm'),
    path('use_add_rating/<film_id>', views.use_add_rating, name='use_add_rating'),
    path('user_view_booked_tickets', views.user_view_booked_tickets, name='user_view_booked_tickets'),
    path('user_view_film_recommendations', views.user_view_film_recommendations, name='user_view_film_recommendations'),
    path('user_view_promotion_details/<filmid>', views.user_view_promotion_details, name='user_view_promotion_details'),
    ################film maker################
    path('filmaker_reg/', views.filmaker_reg, name='filmaker_reg'),
    path('filmaker_home/', views.filmaker_home, name='filmaker_home'),
    path('filmmaker_view_prof', views.filmmaker_view_prof, name='filmmaker_view_prof'),
    path('film_maker_view_theaters/<int:film_id>/', views.film_maker_view_theaters, name='film_maker_view_theaters'),
    path('film_maker_book_seats/<theater_id>/<screening_slot_id>',views.film_maker_book_seats,name='film_maker_book_seats'),
    path('film_maker_seat_confirm/', views.film_maker_seat_confirm, name='film_maker_seat_confirm'),
    path('film_maker_view_campaigns/', views.film_maker_view_campaigns, name='film_maker_view_campaigns'),
    path('film_maker_view_campaigns_basedon_films/<film_id>', views.film_maker_view_campaigns_basedon_films, name='film_maker_view_campaigns_basedon_films'),
    path('film_update_profile/<id>', views.film_update_profile, name='film_update_profile'),
    path('film_maker_view_mssges', views.film_maker_view_mssges, name='film_maker_view_mssges'),
    path('film_maker_chat_owners/<id>', views.film_maker_chat_owners, name='film_maker_chat_owners'),
    path('film_maker_view_tickets', views.film_maker_view_tickets, name='film_maker_view_tickets'),
    path('film_maker_view_producermsg', views.film_maker_view_producermsg, name='film_maker_view_producermsg'),
    path('film_maker_view_films', views.film_maker_view_films, name='film_maker_view_films'),
    path('film_maker_view_theater_book_status', views.film_maker_view_theater_book_status, name='film_maker_view_theater_book_status'),
    path('film_maker_add_promotion_materials/<film_id>', views.film_maker_add_promotion_materials, name='film_maker_add_promotion_materials'),
    path('delete_promo_materials/<int:promo_id>/', views.delete_promo_materials, name='delete_promo_materials'),
    path('film_maker_book_theater/<theater_id>/<int:film_id>/', views.film_maker_book_theater, name='film_maker_book_theater'),
    path('make_payment_for_therate_booking/<theater_id>', views.make_payment_for_therate_booking, name='make_payment_for_therate_booking'),

    #####################content manager#####################
    path('content_manager_reg', views.content_manager_reg, name='content_manager_reg'),
    path('content_manager_home', views.content_manager_home, name='content_manager_home'),
    path('conter_manager_view_prof', views.conter_manager_view_prof, name='conter_manager_view_prof'),
    path('conter_manager_view_films_to_make_campaign', views.conter_manager_view_films_to_make_campaign, name='conter_manager_view_films_to_make_campaign'),
    path('content_manager_manage_campaigns/<film_id>/<film_m_id>', views.content_manager_manage_campaigns, name='content_manager_manage_campaigns'),
    path('update_campaign/<cam_id>', views.update_campaign, name='update_campaign'),
    path('conter_manager_view_promo/<film_id>', views.conter_manager_view_promo, name='conter_manager_view_promo'),
    path('content_manager_view_review&ratings/<filmid>', views.content_manager_view_reviewratings, name='content_manager_view_review&ratings'),
    path('accept_promo_material/<int:promo_id>/', views.accept_promo_material, name='accept_promo_material'),
    path('reject_promo_material/<int:promo_id>/', views.reject_promo_material, name='reject_promo_material'),


    ##############################User App#######################
    path('user_app_login',views.user_app_login,name="user_app_login"),
    path('user_app_signup',views.user_app_signup,name="user_app_signup"),
    path('user_app_view_films',views.user_app_view_films,name="user_app_view_films"),
    path('user_app_view_theaters',views.user_app_view_theaters,name="user_app_view_theaters"),
    path('user_app_view_seats_to_book',views.user_app_view_seats_to_book,name="user_app_view_seats_to_book"),
    path('user_app_seat_booking',views.user_app_seat_booking,name="user_app_seat_booking"),
    path('user_view_app_nots',views.user_view_app_nots,name="user_view_app_nots"),
    path('user_view_app_bookings',views.user_view_app_bookings,name="user_view_app_bookings"),
    path('user_app_add_rating',views.user_app_add_rating,name="user_app_add_rating"),
    path('user_app_search_films',views.user_app_search_films,name="user_app_search_films"),
    path('user_app_view_film_recommendations',views.user_app_view_film_recommendations,name="user_app_view_film_recommendations"),
    path('user_view_app_complaint',views.user_view_app_complaint,name="user_view_app_complaint"),
    path('user_app_send_complaint',views.user_app_send_complaint,name="user_app_send_complaint"),
    

]