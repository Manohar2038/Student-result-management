from flask import Blueprint, request, jsonify
from app import get_db
from app.utils.validators import validate_bulk

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports/full', methods=['GET'])
def full_report():
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT s.id AS student_id, s.name AS student_name, s.roll_number,
               s.department, r.gpa, r.grade,
               sub.code AS subject_code, sub.name AS subject_name, md.marks
        FROM students s
        JOIN results      r   ON s.id         = r.student_id
        JOIN enrollments  e   ON s.id         = e.student_id
        JOIN subjects     sub ON e.subject_id = sub.id
        JOIN marks_detail md  ON md.student_id = s.id AND md.subject_id = sub.id
        ORDER BY s.name, sub.code
    """)
    rows = cur.fetchall()
    return jsonify({'status': 'success', 'count': len(rows), 'data': rows}), 200


@reports_bp.route('/reports/above-avg', methods=['GET'])
def above_avg():
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT s.name, s.department, r.gpa,
               (SELECT ROUND(AVG(r2.gpa), 2)
                FROM results r2 JOIN students s2 ON r2.student_id = s2.id
                WHERE s2.department = s.department) AS dept_avg
        FROM students s
        JOIN results r ON s.id = r.student_id
        WHERE r.gpa > (
            SELECT AVG(r3.gpa)
            FROM results r3 JOIN students s3 ON r3.student_id = s3.id
            WHERE s3.department = s.department
        )
        ORDER BY s.department, r.gpa DESC
    """)
    rows = cur.fetchall()
    return jsonify({'status': 'success', 'count': len(rows), 'data': rows}), 200


@reports_bp.route('/batch/grade-update', methods=['POST'])
def batch_grade_update():
    try:
        db  = get_db()
        cur = db.cursor()
        cur.callproc('recalculate_grades')
        db.commit()
        return jsonify({'status': 'success', 'procedure': 'recalculate_grades', 'transaction': 'COMMIT'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e), 'transaction': 'ROLLBACK'}), 500


@reports_bp.route('/batch/bulk-update', methods=['PUT'])
def bulk_update():
    records = request.get_json()
    ok, err = validate_bulk(records)
    if not ok:
        return jsonify({'status': 'error', 'message': err}), 400

    try:
        db  = get_db()
        cur = db.cursor()
        cur.execute("START TRANSACTION")
        for rec in records:
            cur.execute("UPDATE results SET gpa = %s, grade = %s WHERE student_id = %s",
                        [rec['gpa'], rec['grade'], rec['id']])
        db.commit()
        return jsonify({'status': 'committed', 'rows_affected': len(records), 'transaction': 'COMMIT'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': str(e), 'transaction': 'ROLLBACK'}), 500