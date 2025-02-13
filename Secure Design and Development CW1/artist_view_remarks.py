from flask import Blueprint, render_template, flash
import mysql.connector

artist_view_remarks_bp = Blueprint('artist_view_remarks', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_view_remarks_bp.route('/artist_view_remarks', methods=['GET'])
def artist_view_remarks():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, remark_text, author_role, created_at
            FROM remarks
            WHERE target_role = 'AT'
        """)
        remarks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        remarks = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_view_remarks.html', remarks=remarks)
