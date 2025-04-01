package com.example.bridgeapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;

import org.json.JSONException;
import org.json.JSONObject;

public class UserSignUp extends AppCompatActivity implements JsonResponse {
    TextInputEditText nameInput, emailInput, phoneInput, preferencesInput, usernameInput, passwordInput;
    MaterialButton signUpButton;
    TextView t1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_sign_up);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        t1=findViewById(R.id.signInLink);

        t1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(),Login.class));
            }
        });

        nameInput = findViewById(R.id.nameInput);
        emailInput = findViewById(R.id.emailInput);
        phoneInput = findViewById(R.id.phoneInput);
        preferencesInput = findViewById(R.id.preferencesInput);
        usernameInput = findViewById(R.id.usernameInput);
        passwordInput = findViewById(R.id.passwordInput);

        signUpButton = findViewById(R.id.signUpButton);

        signUpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name = nameInput.getText().toString();
                String email = emailInput.getText().toString();
                String phone = phoneInput.getText().toString();
                String preferences = preferencesInput.getText().toString();
                String username = usernameInput.getText().toString();
                String password = passwordInput.getText().toString();

                JsonReq jr = new JsonReq();
                jr.json_response = UserSignUp.this;
                String q = "/user_app_signup?name=" + name + "&email=" + email + "&phone=" + phone + "&preferences=" + preferences + "&username=" + username + "&password=" + password;
                jr.execute(q);
            }
        });
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        String status = jo.getString("status");

        if (status.equalsIgnoreCase("success")) {
            Toast.makeText(this, "Success", Toast.LENGTH_SHORT).show();
            startActivity(new Intent(getApplicationContext(), Login.class));
        } else {
            Toast.makeText(this, "Failed", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        // Not implemented
    }
}