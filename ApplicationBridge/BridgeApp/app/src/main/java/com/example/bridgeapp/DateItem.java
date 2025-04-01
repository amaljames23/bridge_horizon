package com.example.bridgeapp;

import java.time.LocalDate;

public class DateItem {
    private LocalDate date;
    private boolean isSelected;

    public DateItem(LocalDate date, boolean isSelected) {
        this.date = date;
        this.isSelected = isSelected;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public boolean isSelected() {
        return isSelected;
    }

    public void setSelected(boolean selected) {
        isSelected = selected;
    }
}