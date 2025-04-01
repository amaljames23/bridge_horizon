package com.example.bridgeapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
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

public class SendComplaint extends AppCompatActivity implements JsonResponse{

    EditText e1,e2;
    ListView l1;
    Button b1;
    String title,description,login_id;
    SharedPreferences sh;
    String[] com_title,com_desc,reply,date,values;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_send_complaint);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        l1=findViewById(R.id.complaint_list);


        JsonReq jr = new JsonReq();
        jr.json_response=SendComplaint.this;
        String q = "/user_view_app_complaint?login_id="+Login.login_id;
        jr.execute(q);


        e1=findViewById(R.id.title);
        b1=findViewById(R.id.complaint_btn);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                title=e1.getText().toString();


                if (title.equalsIgnoreCase("")) {
                    e1.setError("title not entered");
                    e1.setFocusable(true);
                } else {
                    JsonReq jr = new JsonReq();
                    jr.json_response = SendComplaint.this;
                    String q = "/user_app_send_complaint?title=" + title + "&login_id=" + Login.login_id;
                    jr.execute(q);
                }
            }
        });
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        try {
            String method=jo.getString("method");
            if (method.equalsIgnoreCase("send")) {
                String status=jo.getString("status");
                if (status.equalsIgnoreCase("success")) {
                    Toast.makeText(this, "success", Toast.LENGTH_SHORT).show();
                    startActivity(new Intent(getApplicationContext(), SendComplaint.class));
                } else {
                    Toast.makeText(this, "failed", Toast.LENGTH_SHORT).show();
                }
            }
            if (method.equalsIgnoreCase("display")) {
                String status=jo.getString("status");
                if (status.equalsIgnoreCase("success")) {
                    JSONArray ja1 = jo.getJSONArray("view");

                    int length = ja1.length();
                    com_title = new String[length];
                    com_desc = new String[length];
                    reply=new String[length];
                    date=new String[length];
                    values=new String[length];


                    for (int i=0;i<length;i++) {
                        com_title[i]=ja1.getJSONObject(i).getString("title");
                        reply[i]=ja1.getJSONObject(i).getString("reply");
                        date[i]=ja1.getJSONObject(i).getString("date");

                        values[i]="title: "+com_title[i]+"\nDate: "+date[i]+"\nreply: "+reply[i];
                    }
                    ArrayAdapter<String> ar = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1, values);
                    l1.setAdapter(ar);

                }
            }

        } catch (Exception e) {
            Toast.makeText(this,e.toString(), Toast.LENGTH_SHORT).show();
//            startActivity(new Intent(getApplicationContext(), UserHome.class));
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }
}