##**Canteen Management System**##

Automating Canteen Operations with QR-Based Meal Tracking

Last Commit: Python, Django

Built with the tools and technologies:
Django HTML CSS JavaScript Bootstrap PostgreSQL MySQL jsQR Pillow OpenCV

Table of Contents

Overview

Features

Installation

Prerequisites

Steps

Usage

Project Structure

Contributing

License

Contact

Overview

The Canteen Management System is a web-based platform designed to streamline and automate canteen operations in corporate or institutional setups.

Key capabilities include:

QR code-based meal logging

Menu management and updates

Daily/Monthly report generation

Attendance tracking for users consuming meals

The system is designed to be scalable, secure, and user-friendly, ensuring minimal manual intervention and accurate data management.

Features

🍽️ QR Code Scanner & Generator: Real-time scanning using webcam or uploaded images.
📊 Automatic Meal Logging: Tracks meal consumption and in-time/out-time for users.
📋 Menu Management: Admin panel to add, edit, delete, and view menu items.
📈 Reports & Analytics: Generate and export daily/monthly reports in CSV, Excel, or PDF.
📱 Responsive Design: Works on both desktop and mobile devices using Bootstrap.

Installation
Prerequisites

Python 3.10+

Django 4.x

PostgreSQL/MySQL

Node JS & npm (optional for frontend enhancements)

Steps

Clone the Repository

git clone <your-repo-url>
cd canteen_management_system


Create Virtual Environment

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install Dependencies

pip install -r requirements.txt


Configure Database

Update settings.py for PostgreSQL/MySQL connection.

Run Migrations

python manage.py makemigrations
python manage.py migrate


Run Server

python manage.py runserver

Usage
Access the Application

Open browser and go to http://127.0.0.1:8000/

Admin Functions

Add/Edit/Delete menu items

Generate daily/monthly meal reports

User Functions

Scan QR code using webcam

Upload QR code image from gallery

Meal consumption automatically logged

Project Structure
canteen_management_system/
├── backend/
│   ├── canteen_app/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   └── static/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── static/
│   ├── templates/
│   └── js/
└── README.md

Contributing

We welcome contributions to enhance the Canteen Management System!

To Contribute:

Fork the repository

Create a feature branch

git checkout -b feature/YourFeature


Commit your changes

git commit -m "Add YourFeature"


Push to your branch

git push origin feature/YourFeature


Open a pull request with a detailed description

✅ Ensure your code passes tests and follows formatting.

License

This project is licensed under the MIT License – see the LICENSE file for details.

Contact

📬 Maintainer: Sanika Shaligram
📧 Email: sanika@example.com
