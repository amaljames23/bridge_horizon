package com.example.bridgeapp;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class UserNotifications extends AppCompatActivity implements JsonResponse{
    ListView l1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_notifications);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        l1=findViewById(R.id.notification_list);

        JsonReq jr = new JsonReq();
        jr.json_response=UserNotifications.this;
        String q = "/user_view_app_nots";
        jr.execute(q);
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");
        if (status.equalsIgnoreCase("success")) {
            JSONArray ja1 = jo.getJSONArray("notifications");

            int length = ja1.length();
            String[] titles = new String[length];
            String[] descriptions = new String[length];
            String[] dates = new String[length];
            String[] values = new String[length];

            for (int i = 0; i < length; i++) {
                JSONObject obj = ja1.getJSONObject(i);
                titles[i] = obj.getString("title");
                descriptions[i] = obj.getString("notifications"); // Fetching notifications field
                dates[i] = obj.getString("date");

                values[i] = "Title: " + titles[i] + "\nNotification: " + descriptions[i] + "\nDate: " + dates[i];
            }

            ArrayAdapter<String> ar = new ArrayAdapter<String>(getApplicationContext(), R.layout.custom_notification_item, values);
            l1.setAdapter(ar);
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}