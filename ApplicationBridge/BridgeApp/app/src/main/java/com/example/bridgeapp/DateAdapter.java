package com.example.bridgeapp;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class DateAdapter extends RecyclerView.Adapter<DateAdapter.DateViewHolder> {

    private List<DateItem> dateItems;
    private Context context;
    private OnDateSelectedListener listener;

    public interface OnDateSelectedListener {
        void onDateSelected(LocalDate date);
    }

    public DateAdapter(Context context, List<DateItem> dateItems, OnDateSelectedListener listener) {
        this.context = context;
        this.dateItems = dateItems;
        this.listener = listener;
    }

    @NonNull
    @Override
    public DateViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.activity_date_item, parent, false);
        return new DateViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DateViewHolder holder, int position) {
        DateItem dateItem = dateItems.get(position);
        LocalDate date = dateItem.getDate();

        // Format day of week (e.g., "MON")
        String dayOfWeek = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            dayOfWeek = date.format(DateTimeFormatter.ofPattern("EEE")).toUpperCase();
        }
        holder.dayTv.setText(dayOfWeek);

        // Format day of month (e.g., "15")
        String dayOfMonth = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            dayOfMonth = date.format(DateTimeFormatter.ofPattern("dd"));
        }
        holder.dateTv.setText(dayOfMonth);

        // Format month (e.g., "JUN")
        String month = null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            month = date.format(DateTimeFormatter.ofPattern("MMM")).toUpperCase();
        }
        holder.monthTv.setText(month);

        // Set selected state
        holder.itemView.setSelected(dateItem.isSelected());

        // Change text color based on selection
        int textColor = dateItem.isSelected() ? Color.GRAY : android.graphics.Color.BLACK;
        holder.dayTv.setTextColor(textColor);
        holder.dateTv.setTextColor(textColor);
        holder.monthTv.setTextColor(textColor);

        holder.itemView.setOnClickListener(v -> {
            // Update selection
            for (DateItem item : dateItems) {
                item.setSelected(false);
            }
            dateItem.setSelected(true);
            notifyDataSetChanged();

            // Notify listener
            if (listener != null) {
                listener.onDateSelected(date);
            }
        });
    }

    @Override
    public int getItemCount() {
        return dateItems.size();
    }

    public static class DateViewHolder extends RecyclerView.ViewHolder {
        TextView dayTv, dateTv, monthTv;

        public DateViewHolder(@NonNull View itemView) {
            super(itemView);
            dayTv = itemView.findViewById(R.id.tv_day);
            dateTv = itemView.findViewById(R.id.tv_date);
            monthTv = itemView.findViewById(R.id.tv_month);
        }
    }
}