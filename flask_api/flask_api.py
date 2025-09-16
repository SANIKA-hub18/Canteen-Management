import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# MySQL Config 
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', '*')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', '*')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '*')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', '*')
#app.config['MYSQL_CHARSET'] = 'utf8'  # No 'utf8mb3' 


mysql = MySQL(app)

# Home Route
@app.route('/', methods=['GET'])
def home():
    return "API is working!"

# Example: Get all users from 'users' table
@app.route('/users', methods=['GET'])
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        cur.close()

        users = []
        for row in rows:
            users.append({'id': row[0], 'name': row[1]})

        return jsonify(users)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Add QR Data to user_meal_history
@app.route('/add_qr_data', methods=['POST'])
def add_qr_data():
    print("🔔 Route hit!")  
    try:
        data = request.get_json(force=True)
        print("📦 Received data:", data)

        user_id = data.get('user_id')
        date = data.get('date')      # format: 'YYYY-MM-DD'
        time = data.get('time')      # format: 'HH:MM:SS'
        meal = data.get('meal')
        qty = data.get('qty')

        print("✅ Parsed:", user_id, date, time, meal, qty)

        # Save to MySQL
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO user_meal_history (user_id, date, time, meal, qty)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, date, time, meal, qty))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Data inserted successfully'})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
