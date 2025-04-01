package com.example.bridgeapp;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class UserBookings extends AppCompatActivity implements JsonResponse {
    ListView l1;
    String[] booking_id, booking_date, payment_status, amount_paid, theater_name, theater_location,image, seat_number, seat_type, slot_start_time, slot_end_time, slot_date, film_name;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_bookings);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        l1=findViewById(R.id.ticket_list);

        JsonReq jr = new JsonReq();
        jr.json_response=UserBookings.this;
        String q = "/user_view_app_bookings?user_id=" + Login.user_id;
        jr.execute(q);
    }


    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");
        String method = jo.getString("method");

        if (method.equalsIgnoreCase("bookings")) {
            if (status.equalsIgnoreCase("success")) {
                JSONArray ja1 = jo.getJSONArray("bookings");
                int length = ja1.length();

                // Initialize arrays
                booking_id = new String[length];
                booking_date = new String[length];
                payment_status = new String[length];
                amount_paid = new String[length];
                theater_name = new String[length];
                theater_location = new String[length];
                seat_number = new String[length];
                seat_type = new String[length];
                slot_start_time = new String[length];
                slot_end_time = new String[length];
                slot_date = new String[length];
                film_name = new String[length];
                image = new String[length];

                for (int i = 0; i < length; i++) {
                    JSONObject bookingObj = ja1.getJSONObject(i);

                    booking_id[i] = String.valueOf(bookingObj.getInt("booking_id"));
                    booking_date[i] = bookingObj.getString("booking_date");
                    payment_status[i] = bookingObj.getString("payment_status");
                    amount_paid[i] = String.valueOf(bookingObj.getDouble("amount_paid"));
                    theater_name[i] = bookingObj.getString("theater_name");
                    theater_location[i] = bookingObj.getString("theater_location");
                    seat_number[i] = bookingObj.getString("seat_number");
                    seat_type[i] = bookingObj.getString("seat_type");
                    slot_start_time[i] = bookingObj.getString("slot_start_time");
                    slot_end_time[i] = bookingObj.getString("slot_end_time");
                    slot_date[i] = bookingObj.getString("slot_date");
                    film_name[i] = bookingObj.getString("film_name");
                    image[i] = bookingObj.getString("image");

                    Toast.makeText(this, "Booking for " + film_name[i], Toast.LENGTH_SHORT).show();
                }

                // Pass data to CustomViewBookings adapter
                CustomViewBookings adapter = new CustomViewBookings(UserBookings.this, booking_id,
                        booking_date, payment_status, amount_paid, theater_name, theater_location,
                        seat_number, seat_type, slot_start_time, slot_end_time, slot_date, film_name, image);
                l1.setAdapter(adapter);
            } else {
                Toast.makeText(this, "No bookings found", Toast.LENGTH_SHORT).show();
            }
        }
    }


    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}