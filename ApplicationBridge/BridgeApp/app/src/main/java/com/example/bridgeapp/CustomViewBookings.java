package com.example.bridgeapp;

import android.app.Activity;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

public class CustomViewBookings extends ArrayAdapter<String> {
    private Activity context;
    SharedPreferences sh;
    private String[] booking_id, booking_date, payment_status, amount_paid,
            theater_name, theater_location, seat_number, seat_type,
            slot_start_time, slot_end_time, slot_date, film_name, image;

    public CustomViewBookings(Activity context, String[] booking_id, String[] booking_date,
                              String[] payment_status, String[] amount_paid, String[] theater_name,
                              String[] theater_location, String[] seat_number, String[] seat_type,
                              String[] slot_start_time, String[] slot_end_time, String[] slot_date,
                              String[] film_name, String[] image) {
        super(context, R.layout.activity_custom_view_bookings, booking_id);
        this.context = context;
        this.booking_id = booking_id;
        this.booking_date = booking_date;
        this.payment_status = payment_status;
        this.amount_paid = amount_paid;
        this.theater_name = theater_name;
        this.theater_location = theater_location;
        this.seat_number = seat_number;
        this.seat_type = seat_type;
        this.slot_start_time = slot_start_time;
        this.slot_end_time = slot_end_time;
        this.slot_date = slot_date;
        this.film_name = film_name;
        this.image = image;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View listItem = inflater.inflate(R.layout.activity_custom_view_bookings, parent, false);

        ImageView filmPoster = listItem.findViewById(R.id.tv_movie_poster);

        TextView tvFilmName = listItem.findViewById(R.id.tv_film_name);
//        TextView tvBookingDate = listItem.findViewById(R.id.tv_booking_date);
        TextView tvPaymentStatus = listItem.findViewById(R.id.tv_payment_status);
        TextView tvAmountPaid = listItem.findViewById(R.id.tv_amount_paid);
        TextView tvTheaterName = listItem.findViewById(R.id.tv_theater_name);
//        TextView tvTheaterLocation = listItem.findViewById(R.id.tv_theater_location);
        TextView tvSeatNumber = listItem.findViewById(R.id.tv_seat_number);
        TextView tvSeatType = listItem.findViewById(R.id.tv_seat_type);
        TextView tvSlotStartTime = listItem.findViewById(R.id.tv_slot_start_time);
//        TextView tvSlotEndTime = listItem.findViewById(R.id.tv_slot_end_time);
        TextView tvSlotDate = listItem.findViewById(R.id.tv_slot_date);

        tvFilmName.setText(film_name[position]);
//        tvBookingDate.setText(booking_date[position]);
        tvPaymentStatus.setText(payment_status[position]);
        tvAmountPaid.setText(amount_paid[position]);
        tvTheaterName.setText(theater_name[position]);
//        tvTheaterLocation.setText(theater_location[position]);
        tvSeatNumber.setText(seat_number[position]);
        tvSeatType.setText(seat_type[position]);
        tvSlotStartTime.setText(slot_start_time[position]);
//        tvSlotEndTime.setText(slot_end_time[position]);
        tvSlotDate.setText(slot_date[position]);

        sh = PreferenceManager.getDefaultSharedPreferences(getContext());
        String imagePath = "http://" + sh.getString("ip", "") + "/static/image/" + image[position];
        imagePath = imagePath.replace("~", ""); // Clean up the image path

        // Load the image using Picasso
        Picasso.with(context)
                .load(imagePath)
                .placeholder(R.drawable.ic_launcher_background) // Placeholder image
                .error(R.drawable.ic_launcher_background) // Error image
                .into(filmPoster);

        return listItem;
    }
}
