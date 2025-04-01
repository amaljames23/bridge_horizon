package com.example.bridgeapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RatingBar;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONException;
import org.json.JSONObject;

public class UserAddRating extends AppCompatActivity implements JsonResponse{
    RatingBar r1;
    EditText e1;
    Button b1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_add_rating);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        r1=findViewById(R.id.ratingBar);
        e1=findViewById(R.id.review);
        b1=findViewById(R.id.rate_btn);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String review=e1.getText().toString();
                float rating=r1.getRating();

                JsonReq jr = new JsonReq();
                jr.json_response = UserAddRating.this;
                String q = "/user_app_add_rating?rating=" + rating + "&review=" + review + "&user_id=" + Login.user_id + "&film_id=" + CustomViewFilms.filmIdLabel; ;
                jr.execute(q);
            }
        });
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        try {
            String status = jo.getString("status");
            if (status.equalsIgnoreCase("success")) {
                Toast.makeText(this, "success", Toast.LENGTH_SHORT).show();
                startActivity(new Intent(getApplicationContext(), UserAddRating.class));
            } else {
                Toast.makeText(this, "failed", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Toast.makeText(this, "error!1", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}