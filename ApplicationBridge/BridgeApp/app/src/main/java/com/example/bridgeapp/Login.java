package com.example.bridgeapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class Login extends AppCompatActivity implements JsonResponse{
    TextView t1,t2;
    EditText e1,e2;
    Button b1;
    String username,password;
    SharedPreferences sh;
    public static  String login_id,user_id,usertype;
    CheckBox c1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_login);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        t1=findViewById(R.id.signup);

        e1=findViewById(R.id.username);
        e2=findViewById(R.id.password);

        b1=findViewById(R.id.login_btn);
        c1 = findViewById(R.id.checkBox);

        c1.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // Show password
                    e2.setInputType(InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
                } else {
                    // Hide password
                    e2.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                }
                // Move cursor to the end of the text
                e2.setSelection(e2.getText().length());
            }
        });

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                username=e1.getText().toString();
                password=e2.getText().toString();

                if (username.equalsIgnoreCase("")) {
                    e1.setError("username not entered");
                    e1.setFocusable(true);
                } else if (password.equalsIgnoreCase("")) {
                    e2.setError("password not entered");
                    e2.setFocusable(true);
                } else {
                    JsonReq jr = new JsonReq();
                    jr.json_response=Login.this;
                    String q = "/user_app_login?username="+username+"&password="+password;
                    jr.execute(q);
                }
            }
        });

        t1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(),UserSignUp.class));
            }
        });
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        try {
            String status=jo.getString("status");
            if (status.equalsIgnoreCase("success")) {
                JSONArray ja1 = jo.getJSONArray("user");

                login_id=ja1.getJSONObject(0).getString("login_id");
                user_id=ja1.getJSONObject(0).getString("user_id");
                usertype=ja1.getJSONObject(0).getString("usertype");

                sh=getSharedPreferences("login", MODE_PRIVATE);
                SharedPreferences.Editor e = sh.edit();

                e.putString("login_id",login_id);
                e.putString("user_id",user_id);
                Toast.makeText(this,user_id, Toast.LENGTH_SHORT).show();
                e.commit();



                if (usertype.equals("user")) {
                    Toast.makeText(this,user_id, Toast.LENGTH_SHORT).show();
                    startActivity(new Intent(getApplicationContext(), UserHome.class));
                }

            } else {
                Toast.makeText(this, "Invalid username or password!", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Toast.makeText(this, "error..", Toast.LENGTH_SHORT).show();
            startActivity(new Intent(getApplicationContext(),IpSetting.class));
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }

    @Override
    public void onBackPressed() {
        startActivity(new Intent(getApplicationContext(),IpSetting.class));
        super.onBackPressed();
    }
}