from flask import Blueprint, request, jsonify
from app import get_db
from app.utils.validators import validate_student, validate_result

students_bp = Blueprint('students', __name__)


@students_bp.route('/students', methods=['GET'])
def get_students():
    dept     = request.args.get('dept')
    semester = request.args.get('semester')
    sort_by  = request.args.get('sort_by', 'id')

    if sort_by not in {'id', 'name', 'gpa', 'semester'}:
        sort_by = 'id'

    sql    = "SELECT s.*, r.gpa, r.grade FROM students s LEFT JOIN results r ON s.id = r.student_id WHERE 1=1"
    params = []

    if dept:
        sql += " AND s.department = %s"
        params.append(dept)
    if semester:
        sql += " AND s.semester = %s"
        params.append(semester)

    sql += f" ORDER BY {sort_by}"

    db  = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return jsonify({'status': 'success', 'count': len(rows), 'data': rows}), 200


@students_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT s.*, r.gpa, r.grade
        FROM students s
        LEFT JOIN results r ON s.id = r.student_id
        WHERE s.id = %s
    """, [id])
    student = cur.fetchone()

    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404

    cur.execute("""
        SELECT sub.code, sub.name AS subject, md.marks
        FROM marks_detail md
        JOIN subjects sub ON md.subject_id = sub.id
        WHERE md.student_id = %s
    """, [id])
    student['subjects'] = cur.fetchall()
    return jsonify({'status': 'success', 'data': student}), 200


@students_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    ok, err = validate_student(data)
    if not ok:
        return jsonify({'status': 'error', 'message': err}), 400

    try:
        db  = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO students (name, roll_number, department, semester)
            VALUES (%s, %s, %s, %s)
        """, [data['name'], data['roll_number'], data['department'], data['semester']])
        db.commit()
        return jsonify({'status': 'created', 'message': 'Student added successfully', 'data': {'id': cur.lastrowid, **data}}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@students_bp.route('/students/<int:id>/results', methods=['PUT'])
def update_result(id):
    data = request.get_json()
    ok, err = validate_result(data)
    if not ok:
        return jsonify({'status': 'error', 'message': err}), 400

    try:
        db  = get_db()
        cur = db.cursor()
        cur.execute("UPDATE results SET gpa = %s, grade = %s WHERE student_id = %s",
                    [data['gpa'], data['grade'], id])
        if cur.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'No result found for this student'}), 404
        db.commit()
        return jsonify({'status': 'success', 'transaction': 'COMMIT', 'data': {'student_id': id, **data}}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e), 'transaction': 'ROLLBACK'}), 500


@students_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM students WHERE id = %s", [id])
    if not cur.fetchone():
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    cur.execute("DELETE FROM students WHERE id = %s", [id])
    db.commit()
    return '', 204