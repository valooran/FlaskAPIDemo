from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# CREATE
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (first_name, last_name, dob, amount_due)
        VALUES (?, ?, ?, ?)
    ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student added successfully'}), 201

# READ ONE
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(dict(student))

# READ ALL
@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

# UPDATE
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        UPDATE students
        SET first_name=?, last_name=?, dob=?, amount_due=?
        WHERE student_id=?
    ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due'], student_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})

# DELETE
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'})

# HOME ROUTE
@app.route('/')
def home():
    return "Welcome to the Student Records API!"

if __name__ == '__main__':
    app.run(debug=True)
