package com.example.bridgeapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.TextView;

public class CustomViewTheaters extends ArrayAdapter<String> {
    private final Activity context;
    private final String[] theater_id;
    private final String[] name;
    private final String[] location;
    private final String[] contact_email;
    private final String[] contact_phone;
    private final int[] capacity;
    private final String[][] slots_start_time;
    private final String[][] slots_status;
    private final String[][] slots_id;
    private final String[][] slots_film_id;

    public static String sl_id,theaterLabel_id,slot_time;

    public CustomViewTheaters(Activity context, String[] theater_id, String[] name,
                              String[] location, String[] contact_email, String[] contact_phone,
                              int[] capacity, String[][] slots_id, String[][] slots_start_time, String[][] slots_status,
                              String[][] slots_film_id) {
        super(context, R.layout.activity_custom_view_theaters, name);
        this.context = context;
        this.theater_id = theater_id;
        this.name = name;
        this.location = location;
        this.contact_email = contact_email;
        this.contact_phone = contact_phone;
        this.capacity = capacity;
        this.slots_id = slots_id;
        this.slots_start_time = slots_start_time;
        this.slots_status = slots_status;
        this.slots_film_id = slots_film_id;
    }

    @Override
    public View getView(int position, View view, ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View rowView = inflater.inflate(R.layout.activity_custom_view_theaters, null, true);

        // Initialize views
        TextView theaterName = rowView.findViewById(R.id.theater_name);
        TextView theaterLocation = rowView.findViewById(R.id.theater_location);
        TextView theaterCapacity = rowView.findViewById(R.id.theater_capacity);
        TextView theaterEmail = rowView.findViewById(R.id.theater_email);
        TextView theaterPhone = rowView.findViewById(R.id.theater_phone);
        LinearLayout slotsContainer = rowView.findViewById(R.id.slots_container);

        // Set theater details
        theaterName.setText(name[position]);
        theaterLocation.setText(location[position]);
        theaterCapacity.setText("Capacity: " + capacity[position] + " seats");
        theaterEmail.setText(contact_email[position]);
        theaterPhone.setText(contact_phone[position]);

        // Add slots dynamically
        for (int i = 0; i < slots_start_time[position].length; i++) {
            final int slotIndex = i;
            View slotView = inflater.inflate(R.layout.layout_show_slot, slotsContainer, false);

            TextView slotTime = slotView.findViewById(R.id.slot_time);
            TextView slotStatus = slotView.findViewById(R.id.slot_status);

            slotTime.setText(slots_start_time[position][i]);
            slotStatus.setText(slots_status[position][i]);

            // Set different background colors based on status
            if (slots_status[position][i].equalsIgnoreCase("available")) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    slotView.setBackgroundTintList(context.getColorStateList(android.R.color.holo_green_light));
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    slotStatus.setTextColor(context.getColor(android.R.color.holo_green_dark));
                }
            } else {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    slotView.setBackgroundTintList(context.getColorStateList(android.R.color.darker_gray));
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    slotStatus.setTextColor(context.getColor(android.R.color.white));
                }
            }

            // Set click listener for each slot
            slotView.setOnClickListener(v -> {
                if (slots_status[position][slotIndex].equalsIgnoreCase("available")) {

                    sl_id = slots_id[position][slotIndex];
                    theaterLabel_id = theater_id[position];
                    slot_time = slots_start_time[position][slotIndex];

                    Intent intent = new Intent(context, UserViewSeats.class);
//                    intent.putExtra("theater_id", theater_id[position]);
//                    intent.putExtra("theater_name", name[position]);
//                    intent.putExtra("slot_time", slots_start_time[position][slotIndex]);
//                    intent.putExtra("film_id", slots_film_id[position][slotIndex]);
                    context.startActivity(intent);
                }
            });

            slotsContainer.addView(slotView);
        }

        return rowView;
    }
}
