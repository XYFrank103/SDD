from flask import Blueprint, render_template, flash, session
import mysql.connector

artist_view_attendance_bp = Blueprint('artist_view_attendance', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_view_attendance_bp.route('/artist_view_attendance', methods=['GET'])
def artist_view_attendance():
    artist_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, user_id, attendance_date 
            FROM attendance 
            WHERE user_id = %s
        """, (artist_id,))
        attendance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        attendance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_view_attendance.html', attendance_records=attendance_records)
