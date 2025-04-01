package com.example.bridgeapp;

import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.GridLayout;
import android.widget.ImageButton;
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

import java.util.ArrayList;
import java.util.List;

public class UserViewSeats extends AppCompatActivity implements JsonResponse {

    String[] seat_id, seat_number, seat_type, seat_status, slot_id;
    GridLayout seatsGrid;
    TextView tvSelectedSeats, tvTotal,tvTime, tvDate;
    Button btnCheckout;
    StringBuilder seatIds;
    ImageButton btnBack;

    // To keep track of selected seats
    List<String> selectedSeats = new ArrayList<>();
    List<String> selectedSeatIds = new ArrayList<>();
    int totalPrice = 0;
    int pricePerSeat = 150; // Default price, you can modify this

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_view_seats);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Initialize views
        seatsGrid = findViewById(R.id.seatsGrid);
        tvSelectedSeats = findViewById(R.id.tvSelectedSeats);
        tvTotal = findViewById(R.id.tvTotal);
        btnCheckout = findViewById(R.id.btnCheckout);
        btnBack = findViewById(R.id.btnBack);
        tvTime=findViewById(R.id.tvTime);
        tvDate=findViewById(R.id.tvDate);

        tvTime.setText(CustomViewTheaters.slot_time);
        tvDate.setText(UserViewTheaters.currentDate);

        // Set back button click listener
        btnBack.setOnClickListener(v -> finish());

        // Set checkout button click listener
        btnCheckout.setOnClickListener(v -> {
            if (selectedSeats.isEmpty()) {
                Toast.makeText(UserViewSeats.this, "Please select at least one seat", Toast.LENGTH_SHORT).show();
            } else {
                // Proceed to checkout
                // You can add your checkout logic here
                seatIds = new StringBuilder();
                for (String id : selectedSeatIds) {
                    seatIds.append(id).append(",");
                }
                if (seatIds.length() > 0) {
                    seatIds.deleteCharAt(seatIds.length() - 1);
                }

                Toast.makeText(UserViewSeats.this, "Proceeding to checkout with seats: " +
                        String.join(", ", selectedSeats) + seatIds, Toast.LENGTH_SHORT).show();


                JsonReq jr = new JsonReq();
                jr.json_response=UserViewSeats.this;
                String q = "/user_app_seat_booking?seat_ids="+seatIds.toString()+"&slot_id="+CustomViewTheaters.sl_id+"&user_id="+Login.user_id+"&theater_id="+CustomViewTheaters.theaterLabel_id+"&film_id="+CustomViewFilms.filmIdLabel+"&tot_price="+totalPrice;
                jr.execute(q);


                // Here you would typically navigate to a checkout activity
                // Intent intent = new Intent(UserViewSeats.this, CheckoutActivity.class);
                // intent.putExtra("selected_seat_ids", seatIds.toString());
                // intent.putExtra("total_price", totalPrice);
                // startActivity(intent);
            }
        });

        // Fetch seats data
        JsonReq jr = new JsonReq();
        jr.json_response = UserViewSeats.this;
        String q = "/user_app_view_seats_to_book?slot_id=" + CustomViewTheaters.sl_id;
        jr.execute(q);
    }

    @Override
    public void response(JSONObject jo) throws JSONException {
        // Get the status from the response
        String status = jo.getString("status");

        if (status.equalsIgnoreCase("success")) {
            // Extract the seats array
            JSONArray seatsArray = jo.getJSONArray("seats");
            int length = seatsArray.length();

            // Initialize arrays
            seat_id = new String[length];
            seat_number = new String[length];
            seat_type = new String[length];
            seat_status = new String[length];
            slot_id = new String[length];

            for (int i = 0; i < length; i++) {
                JSONObject seatObj = seatsArray.getJSONObject(i);

                seat_id[i] = seatObj.getString("seat_id");
                seat_number[i] = seatObj.getString("seat_number");
                seat_type[i] = seatObj.getString("seat_type");
                seat_status[i] = seatObj.getString("status");
                slot_id[i] = seatObj.getString("slot_id");
            }

            // Now populate the seats grid
            populateSeatsGrid();
        } else {
            Toast.makeText(this, "No seats available", Toast.LENGTH_SHORT).show();
        }
    }

    private void populateSeatsGrid() {
        // Clear the grid first
        seatsGrid.removeAllViews();

        // Calculate how many rows and columns we need
        int totalSeats = seat_id.length;
        int columns = 8; // As per your design
        int rows = (int) Math.ceil((double) totalSeats / columns);

        // Set the grid properties
        seatsGrid.setColumnCount(columns);
        seatsGrid.setRowCount(rows);

        // Add seats to the grid
        for (int i = 0; i < totalSeats; i++) {
            // Create a frame layout to hold the seat and its number
            FrameLayout seatFrame = new FrameLayout(this);
            GridLayout.LayoutParams params = new GridLayout.LayoutParams();
            params.width = 48; // Width in dp
            params.height = 48; // Height in dp
            params.setMargins(6, 6, 6, 6); // Margins in dp

            // Calculate row and column
            int row = i / columns;
            int col = i % columns;

            // Set row and column in GridLayout
            params.rowSpec = GridLayout.spec(row);
            params.columnSpec = GridLayout.spec(col);

            // Set layout parameters
            seatFrame.setLayoutParams(params);

            // Create the seat background view
            View seatBackground = new View(this);
            FrameLayout.LayoutParams bgParams = new FrameLayout.LayoutParams(
                    FrameLayout.LayoutParams.MATCH_PARENT,
                    FrameLayout.LayoutParams.MATCH_PARENT
            );
            seatBackground.setLayoutParams(bgParams);

            // Create the seat number text view
            TextView seatNumberView = new TextView(this);
            FrameLayout.LayoutParams textParams = new FrameLayout.LayoutParams(
                    FrameLayout.LayoutParams.WRAP_CONTENT,
                    FrameLayout.LayoutParams.WRAP_CONTENT
            );
            textParams.gravity = Gravity.CENTER;
            seatNumberView.setLayoutParams(textParams);
            seatNumberView.setText(seat_number[i]);
            seatNumberView.setTextSize(10); // Small text size
            seatNumberView.setGravity(Gravity.CENTER);

            // Set background color based on seat status
            if (seat_status[i].equalsIgnoreCase("booked")) {
                // Reserved seat
                seatBackground.setBackgroundColor(Color.parseColor("#6E6E9E"));
                seatNumberView.setTextColor(Color.WHITE);
                seatFrame.setClickable(false);
            } else {
                // Available seat
                seatBackground.setBackgroundResource(R.drawable.seat_available_border);
                seatNumberView.setTextColor(Color.parseColor("#FF3B30"));

                // Set tag to identify the seat
                seatFrame.setTag(i);

                // Set click listener
                seatFrame.setOnClickListener(v -> {
                    int position = (int) v.getTag();
                    toggleSeatSelection(v, position);
                });
            }

            // Add views to frame
            seatFrame.addView(seatBackground);
            seatFrame.addView(seatNumberView);

            // Add to grid
            seatsGrid.addView(seatFrame);
        }
    }

    private void toggleSeatSelection(View seatView, int position) {
        String seatId = seat_id[position];
        String seatNumber = seat_number[position];

        // Get the background view (first child of FrameLayout)
        View seatBackground = ((FrameLayout) seatView).getChildAt(0);
        // Get the text view (second child of FrameLayout)
        TextView seatNumberView = (TextView) ((FrameLayout) seatView).getChildAt(1);

        if (selectedSeatIds.contains(seatId)) {
            // Deselect the seat
            selectedSeatIds.remove(seatId);
            selectedSeats.remove(seatNumber);
            seatBackground.setBackgroundResource(R.drawable.seat_available_border);
            seatNumberView.setTextColor(Color.parseColor("#FF3B30"));
            totalPrice -= pricePerSeat;
        } else {
            // Select the seat
            selectedSeatIds.add(seatId);
            selectedSeats.add(seatNumber);
            seatBackground.setBackgroundColor(Color.parseColor("#FF3B30"));
            seatNumberView.setTextColor(Color.WHITE);
            totalPrice += pricePerSeat;
        }

        // Update UI
        updateSelectedSeatsUI();
    }

    private void updateSelectedSeatsUI() {
        if (selectedSeats.isEmpty()) {
            tvSelectedSeats.setText("None");
            tvTotal.setText("₹0");
        } else {
            tvSelectedSeats.setText(String.join(", ", selectedSeats));
            tvTotal.setText("₹" + totalPrice);
        }
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        // Not used in this implementation
    }
}