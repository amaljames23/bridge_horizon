package com.example.bridgeapp;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class Recommendation extends AppCompatActivity implements JsonResponse {

    String[] filmid, film_name, filmmaker, details, photo, date;
    GridView g1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_recommendation);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        g1=findViewById(R.id.film_lists);

        JsonReq jr = new JsonReq();
        jr.json_response=Recommendation.this;
        String q = "/user_app_view_film_recommendations";
        jr.execute(q);
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");
        String method = jo.getString("method");
        if (method.equalsIgnoreCase("film_recommendations")) {
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
                CustomViewFilms adapter = new CustomViewFilms(Recommendation.this, filmid,
                        film_name, filmmaker, details, photo, date, average_rating);
                g1.setAdapter(adapter);
            } else {
                Toast.makeText(this, "No films found", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}