from flask import Blueprint, render_template, flash, session
import mysql.connector

director_view_attendance_bp = Blueprint('director_view_attendance', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_view_attendance_bp.route('/director_view_attendance', methods=['GET'])
def director_view_attendance():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        director_id = session.get('user_id')

        cursor.execute("""
            SELECT id, user_id, attendance_date 
            FROM attendance 
            WHERE user_id = %s
        """, (director_id,))
        attendance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        attendance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_view_attendance.html', attendance_records=attendance_records)
