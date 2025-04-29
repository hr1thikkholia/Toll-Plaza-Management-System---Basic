import sqlite3

def create_table():
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tolls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_number TEXT,
                    vehicle_type TEXT,
                    toll_amount REAL,
                    timestamp TEXT,
                    lane_number TEXT
                )''')
    conn.commit()
    conn.close()

def add_record(vehicle_number, vehicle_type, toll_amount, timestamp, lane_number):
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tolls (vehicle_number, vehicle_type, toll_amount, timestamp, lane_number)
                 VALUES (?, ?, ?, ?, ?)''',
              (vehicle_number, vehicle_type, toll_amount, timestamp, lane_number))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tolls")
    data = c.fetchall()
    conn.close()
    return data

def search_records(vehicle_number):
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tolls WHERE vehicle_number LIKE ?", ('%' + vehicle_number + '%',))
    data = c.fetchall()
    conn.close()
    return data

def delete_record(record_id):
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute("DELETE FROM tolls WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

def update_record(record_id, vehicle_number, vehicle_type, toll_amount, timestamp, lane_number):
    conn = sqlite3.connect('toll_records.db')
    c = conn.cursor()
    c.execute('''UPDATE tolls SET
                    vehicle_number=?,
                    vehicle_type=?,
                    toll_amount=?,
                    timestamp=?,
                    lane_number=?
                 WHERE id=?''',
              (vehicle_number, vehicle_type, toll_amount, timestamp, lane_number, record_id))
    conn.commit()
    conn.close()
