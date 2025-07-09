from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def store_booking(data):
    conn = sqlite3.connect('../database/bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            service TEXT,
            date TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    cursor.execute('''
        INSERT INTO bookings (name, email, service, date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['email'], data['service'], data['date'], 'pending'))
    conn.commit()
    conn.close()

@app.route('/book', methods=['POST'])
def book_service():
    data = request.get_json()
    store_booking(data)
    return jsonify({'message': 'Booking received! We’ll confirm shortly.'})

@app.route('/bookings', methods=['GET'])
def get_bookings():
    conn = sqlite3.connect('../database/bookings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, service, date, status FROM bookings ORDER BY date')
    rows = cursor.fetchall()
    conn.close()

    bookings = [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'service': row[3],
            'date': row[4],
            'status': row[5]
        }
        for row in rows
    ]
    return jsonify(bookings)

@app.route('/complete/<int:booking_id>', methods=['POST'])
def mark_completed(booking_id):
    conn = sqlite3.connect('../database/bookings.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', ('completed', booking_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Booking marked as completed'})

if __name__ == '__main__':
    app.run(debug=True)