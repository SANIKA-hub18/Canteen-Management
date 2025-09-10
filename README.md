<h1>Canteen Management System</h1>

<p><strong>Overview</strong></p>
<p>
Canteen Management System is a web-based application built with <strong>Django</strong> and <strong>PostgreSQL</strong>.  
It streamlines canteen operations like <strong>meal ordering</strong>, <strong>QR code scanning</strong>, and <strong>report generation</strong>.  
Admins can manage menu items, upload menu cards, and track consumption efficiently.
</p>

<h2>🚀 Features</h2>
<ul>
  <li><strong>QR Code Based Transactions</strong> – Instant scan & verification of meals</li>
  <li><strong>Admin Dashboard</strong> – Manage, edit, and delete menu items</li>
  <li><strong>Reports</strong> – Generate daily/monthly reports in <strong>CSV</strong>, <strong>Excel</strong>, and <strong>PDF</strong></li>
  <li><strong>Upload Menu</strong> – Upload and preview canteen menu card</li>
  <li><strong>User-Friendly UI</strong> – Responsive design built with <strong>Bootstrap</strong></li>
</ul>

<h2>⚙️ Installation</h2>
<ol>
  <li>Clone the Repository</li>

```bash
git clone https://github.com/yourusername/canteen-management.git
cd canteen-management
<li>Create Virtual Environment & Install Requirements</li>
bash
Copy code
python -m venv venv
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate

pip install -r requirements.txt
<li>Apply Migrations</li>
bash
Copy code
python manage.py migrate
<li>Run the Server</li>
bash
Copy code
python manage.py runserver
</ol> <h2>📂 Project Structure</h2>
csharp
Copy code
canteen_management/
├── canteen/            # Main Django app
├── templates/          # HTML templates
├── static/             # CSS, JS, Images
├── manage.py
└── requirements.txt
<h2>🤝 Contributing</h2> <p> Contributions are welcome! Please fork the repo and create a feature branch: </p>
bash
Copy code
git checkout -b feature/YourFeature
git commit -m "Add YourFeature"
git push origin feature/YourFeature
<h2>📧 Contact</h2> <p> <strong>Maintainer:</strong> Sanika Shaligram <br> <strong>Email:</strong> shaligramsanika@gmail.com </p> ```
