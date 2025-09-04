from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# MySQL DB Config - तुमचा MySQL user, password, host, port, db name इथे टाका
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost:3306/qr_qrdata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model - Muster table साठी
class Muster(db.Model):
    __tablename__ = 'muster'  # तुमचा table नाव
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)  # तुम्हाला QR data कुठे save करायचं ते field
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Muster {self.data}>'

# Route - QR data POST करून save करणारा
@app.route('/save_qr', methods=['POST'])
def save_qr():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    new_entry = Muster(data=data)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Data saved', 'id': new_entry.id}), 201

if __name__ == '__main__':
    # DB table create करायची असेल तर uncomment करा खालील line
    # db.create_all()
    app.run(debug=True)
