# 🏏 Online Cricket Bidding System

A modern Django-based Cricket Auction & Bidding Platform inspired by IPL-style live auctions.

This project allows admins to create auctions, manage teams and players, conduct live bidding, track team wallets, and generate auction summaries with analytics dashboards.

---

# 🚀 Features

## 🔐 Authentication System
- User Registration
- Secure Login
- User Profile Management
- Protected Dashboards

---

# 🏏 Auction Management

Admins can:

- Create Auctions
- Set Auction Date
- Set Team Purse Amount
- Configure:
  - Minimum Bid
  - Bid Increment
  - Players Per Team

---

# 👥 Player Management

Add players with:

- Player Photo
- Name
- Category
- Mobile Number
- Email
- Date of Birth
- Jersey Sizes
- Notes

Player Categories:
- Right Hand Batsman
- Left Hand Batsman
- All Rounders
- Bowlers
- Wicket Keepers

---

# 🏆 Team Management

Create teams with:
- Team Logo
- Team Name
- Dynamic Purse Wallet

---

# ⚡ Live Bidding Dashboard

Professional real-time bidding dashboard with:

- Live Player Display
- Team Bidding Buttons
- Auto Bid Increase
- Sold / Unsold Actions
- Undo / Reset Functionality
- Random Player Selection
- Auction Flow Control

---

# 💰 Wallet System

Each team gets:
- Starting Purse
- Remaining Balance
- Spent Amount Tracking

Wallet automatically updates after player purchase.

---

# 📊 Auction Summary

Modern analytics dashboard including:

- Team Squads
- Sold Players
- Unsold Players
- Team Spending
- Remaining Purse
- Animated Vertical Bid Graph

---

# 🎨 UI Features

- Modern Responsive Design
- Glassmorphism Effects
- Animated Dashboard
- Dynamic Graphs
- Smooth Scrolling
- Interactive Cards
- Beautiful Landing Page

---

# 🛠 Tech Stack

## Backend
- Django 5
- Python 3.12

## Frontend
- HTML5
- CSS3
- JavaScript

## Database
- SQLite3

---

# 📂 Project Structure

```bash
cricket_bidding/
│
├── home/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   └── urls.py
│
├── media/
├── db.sqlite3
├── manage.py
└── requirements.txt
