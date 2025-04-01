package com.example.bridgeapp;

import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class UserViewTheaters extends AppCompatActivity implements JsonResponse, AdapterView.OnItemClickListener, DateAdapter.OnDateSelectedListener  {
    ListView l1;
    RecyclerView dateRecyclerView;
    DateAdapter dateAdapter;
    public static String currentDate;
    List<DateItem> dateItems;;
    DateTimeFormatter formatter;

    // Declare arrays to store theater data
    String[] theater_id, name, location, contact_email, contact_phone;
    int[] capacity;
    String[][] slots_start_time, slots_status, slots_film_id,slots_id; // Nested array for slots

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_view_theaters);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        l1 = findViewById(R.id.theaters_list);
//        l1.setOnItemClickListener(this);

        DateTimeFormatter formatter = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
            currentDate = LocalDate.now().format(formatter);
        }

        dateRecyclerView = findViewById(R.id.date_recycler_view);
        dateRecyclerView.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false));

        // Create date items for next 7 days
        dateItems = new ArrayList<>();
        LocalDate today = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            today = LocalDate.now();
        }

        for (int i = 0; i < 7; i++) {
            LocalDate date = null;
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                date = today.plusDays(i);
            }
            boolean isSelected = i == 0; // Select today by default
            dateItems.add(new DateItem(date, isSelected));
        }

        // Set up adapter
        dateAdapter = new DateAdapter(this, dateItems,this);
        dateRecyclerView.setAdapter(dateAdapter);

        // Set initial date
        formatter = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            currentDate = today.format(formatter);
        }

//        JsonReq jr = new JsonReq();
//        jr.json_response = UserViewTheaters.this;
//        String q = "/user_app_view_theaters?film_id=" + CustomViewFilms.filmIdLabel + "&date=" + currentDate;
//        jr.execute(q);
        loadTheaters();
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");
        Toast.makeText(this,status, Toast.LENGTH_SHORT).show();
        if (status.equalsIgnoreCase("success")) {
            JSONArray theatersArray = jo.getJSONArray("theaters");
            int length = theatersArray.length();

            // Initialize arrays
            theater_id = new String[length];
            name = new String[length];
            location = new String[length];
            contact_email = new String[length];
            contact_phone = new String[length];
            capacity = new int[length];

            slots_id = new String[length][];
            slots_start_time = new String[length][];
            slots_status = new String[length][];
            slots_film_id = new String[length][];

            for (int i = 0; i < length; i++) {
                JSONObject theaterObj = theatersArray.getJSONObject(i);

                theater_id[i] = theaterObj.getString("theater_id");
                name[i] = theaterObj.getString("name");
                location[i] = theaterObj.getString("location");
                contact_email[i] = theaterObj.getString("contact_email");
                contact_phone[i] = theaterObj.getString("contact_phone");
                capacity[i] = theaterObj.getInt("capacity");

                JSONArray slotsArray = theaterObj.getJSONArray("slots");
                int slotLength = slotsArray.length();

                slots_id[i] = new String[slotLength];
                slots_start_time[i] = new String[slotLength];
                slots_status[i] = new String[slotLength];
                slots_film_id[i] = new String[slotLength];

                for (int j = 0; j < slotLength; j++) {
                    JSONObject slotObj = slotsArray.getJSONObject(j);
                    slots_id[i][j] = slotObj.getString("slot_id");
                    slots_start_time[i][j] = slotObj.getString("start_time");
                    slots_status[i][j] = slotObj.getString("status");
                    slots_film_id[i][j] = slotObj.getString("film_id");
                }
            }

            // Pass data to CustomViewTheaters adapter
            CustomViewTheaters adapter = new CustomViewTheaters(
                    this, theater_id, name, location, contact_email, contact_phone, capacity, slots_id, slots_start_time, slots_status, slots_film_id);
            l1.setAdapter(adapter);
        } else {
            Toast.makeText(this, "No theaters found", Toast.LENGTH_SHORT).show();
        }
    }
    private void loadTheaters() {
        JsonReq jr = new JsonReq();
        jr.json_response = UserViewTheaters.this;
        String q = "/user_app_view_theaters?film_id=" + CustomViewFilms.filmIdLabel + "&date=" + currentDate;
        jr.execute(q);
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        Toast.makeText(this, "Selected: " + name[i], Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onDateSelected(LocalDate date) {
        DateTimeFormatter formatter = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            currentDate = date.format(formatter);
        }

        loadTheaters();

        // Show toast to indicate date selection
//        Toast.makeText(this, "Selected date: " + currentDate, Toast.LENGTH_SHORT).show();
    }
}
