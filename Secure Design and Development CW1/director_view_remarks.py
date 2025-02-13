from flask import Blueprint, render_template, flash
import mysql.connector

director_view_remarks_bp = Blueprint('director_view_remarks', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_view_remarks_bp.route('/director_view_remarks', methods=['GET'])
def director_view_remarks():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, remark_text, created_at 
            FROM remarks 
            WHERE author_role = 'Admin' AND target_role = 'DR'
        """)
        remarks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        remarks = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_view_remarks.html', remarks=remarks)
