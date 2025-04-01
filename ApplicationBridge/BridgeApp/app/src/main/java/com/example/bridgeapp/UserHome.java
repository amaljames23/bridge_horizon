package com.example.bridgeapp;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class UserHome extends AppCompatActivity implements JsonResponse{
    GridView g1;
    ImageButton b1,b2;
    EditText search;
    String[] filmid, film_name, filmmaker, details, photo, date;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_home);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        b2=findViewById(R.id.btn_complaints);

        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(),SendComplaint.class));
            }
        });

        search = findViewById(R.id.et_search);

        search.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.toString().trim().isEmpty()) {
                    // If the search text is empty, send request to view all films
                    sendViewAllFilmsRequest();
                } else {
                    // Otherwise, send the search request
                    sendSearchRequest(s.toString());
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        g1=findViewById(R.id.film_lists);
        b1=findViewById(R.id.btn_notifications);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(),UserNotifications.class));
            }
        });

        JsonReq jr = new JsonReq();
        jr.json_response=UserHome.this;
        String q = "/user_app_view_films";
        jr.execute(q);

        BottomNavigationView bottomNavigationView = findViewById(R.id.bottom_navigation);

        // Set up item selection listener
        bottomNavigationView.setOnItemSelectedListener(item -> {
            int itemId = item.getItemId();

            if (itemId == R.id.nav_home) {
                // Navigate to MainActivity when Jobs tab is clicked
                Intent intent = new Intent(UserHome.this, UserHome.class);
                startActivity(intent);
                return true;
            } else if (itemId == R.id.nav_home) {
                // Already in the home screen, do nothing or refresh
                return true;
            } else if (itemId == R.id.nav_bookings) {
                // TODO: Navigate to Experts activity
                Intent intent = new Intent(UserHome.this, UserBookings.class);
                startActivity(intent);
                return true;
            } else if (itemId == R.id.nav_profile) {
                // TODO: Navigate to Profile activity
                Intent intent = new Intent(UserHome.this, Recommendation.class);
                startActivity(intent);
                return true;
            }

            return false;
        });
    }

    private void sendSearchRequest(String query) {
        JsonReq jr = new JsonReq();
        jr.json_response = UserHome.this;
        String q = "/user_app_search_films?q=" + query; // Append query parameter
        jr.execute(q);
    }

    // Function to send request when search is empty
    private void sendViewAllFilmsRequest() {
        JsonReq jr = new JsonReq();
        jr.json_response = UserHome.this;
        String q = "/user_app_view_films";
        jr.execute(q);
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");
        String method = jo.getString("method");
        if (method.equalsIgnoreCase("films")) {
            if (status.equalsIgnoreCase("success")) {
                JSONArray ja1 = jo.getJSONArray("films");
                int length = ja1.length();

                // Initialize arrays
                filmid = new String[length];
                film_name = new String[length];
                filmmaker = new String[length];
                details = new String[length];
                photo = new String[length];
                date = new String[length];
                double[] average_rating = new double[length]; // Add this array

                for (int i = 0; i < length; i++) {
                    JSONObject filmObj = ja1.getJSONObject(i);

                    filmid[i] = filmObj.getString("filmid");
                    film_name[i] = filmObj.getString("film_name");
                    filmmaker[i] = filmObj.getString("filmmaker");
                    details[i] = filmObj.getString("details");
                    photo[i] = filmObj.getString("photo");
                    date[i] = filmObj.getString("date");
                    average_rating[i] = filmObj.getDouble("average_rating"); // Get the rating

                    Toast.makeText(this, film_name[i], Toast.LENGTH_SHORT).show();
                }

                // Pass data to CustomViewFilms adapter including the average_rating
                CustomViewFilms adapter = new CustomViewFilms(UserHome.this, filmid,
                        film_name, filmmaker, details, photo, date, average_rating);
                g1.setAdapter(adapter);
            } else {
                Toast.makeText(this, "No films found", Toast.LENGTH_SHORT).show();
                CustomViewFilms adapter = new CustomViewFilms(UserHome.this, new String[0],
                        new String[0], new String[0], new String[0], new String[0], new String[0], new double[0]);
                g1.setAdapter(adapter);
            }
        }
    }


    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}

