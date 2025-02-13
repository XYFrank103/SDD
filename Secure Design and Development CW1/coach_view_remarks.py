from flask import Blueprint, render_template, flash
import mysql.connector

coach_view_remarks_bp = Blueprint('coach_view_remarks', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@coach_view_remarks_bp.route('/coach_view_remarks', methods=['GET'])
def coach_view_remarks():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("SELECT remark_text, author_role, created_at FROM remarks WHERE author_role = 'Admin' AND target_role = 'CH'")
        remarks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        remarks = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('coach_view_remarks.html', remarks=remarks)
