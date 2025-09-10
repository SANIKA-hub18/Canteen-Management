<h1 align="center">🍴 Canteen Management System</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Django-3.2-green?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10-yellow?logo=python&logoColor=white" />
</p>

---

<h2>📖 Overview</h2>
<p>
Canteen Management System is a web-based application built with <strong>Django</strong> and <strong>MySQL</strong>.  
It simplifies and automates canteen operations like <strong>meal ordering</strong>, <strong>QR code scanning</strong>, and <strong>report generation</strong>.  
Admins can manage menu items, upload menu cards, and track consumption seamlessly.
</p>

---

<h2>✨ Features</h2>
<ul>
  <li><strong>QR Code Based Transactions</strong> – Fast scan & verification of meals</li>
  <li><strong>Admin Dashboard</strong> – Add, edit, and delete menu items</li>
  <li><strong>Reports</strong> – Download daily/monthly reports in <strong>CSV</strong>, <strong>Excel</strong>, and <strong>PDF</strong></li>
  <li><strong>Upload Menu</strong> – Upload & preview canteen menu card with delete option</li>
  <li><strong>User-Friendly UI</strong> – Responsive and mobile-friendly design using Bootstrap</li>
</ul>

---

<h2>⚙️ Installation</h2>
<ol>
  <li>Clone the Repository</li>
  <pre><code>git clone https://github.com/SANIKA-hub18/canteen-management.git
cd canteen-management</code></pre>

  <li>Create Virtual Environment & Install Dependencies</li>
  <pre><code>python -m venv venv
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate

pip install -r requirements.txt</code></pre>

  <li>Apply Migrations</li>
  <pre><code>python manage.py migrate</code></pre>

  <li>Run the Development Server</li>
  <pre><code>python manage.py runserver</code></pre>
</ol>

<h2>📂 Project Structure</h2>
<pre>
canteen_management/
├── canteen/            # Main Django app
├── templates/          # HTML templates
├── static/             # CSS, JS, Images
├── manage.py
└── requirements.txt
</pre>

<h2>🤝 Contributing</h2>
<p>
Contributions are always welcome! To contribute, fork the repository and create a feature branch:
</p>
<pre><code>git checkout -b feature/YourFeature
git commit -m "Add YourFeature"
git push origin feature/YourFeature
</code></pre>
<p>Then open a Pull Request 🚀</p>

<h2>📧 Contact</h2>
<p>
<strong>Maintainer:</strong> Sanika Shaligram <br>
<strong>Email:</strong> shaligramsanika@gmail.com
</p>
