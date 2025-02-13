from flask import render_template, session, flash, redirect, url_for
import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

def user_attendance():
    user_id = session.get('user_id')

    if not user_id:
        flash('You need to log in to view your attendance records.', 'danger')
        return redirect(url_for('login'))

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM attendance WHERE user_id = %s", (user_id,))
        attendance_records = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        attendance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('user_attendance.html', attendance_records=attendance_records)
