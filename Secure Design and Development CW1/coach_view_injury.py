from flask import Blueprint, render_template, flash
import mysql.connector

coach_view_injury_bp = Blueprint('coach_view_injury', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@coach_view_injury_bp.route('/coach_view_injury', methods=['GET'])
def coach_view_injury():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT injuries.user_id, injuries.injury_date
            FROM injuries
            JOIN users ON injuries.user_id = users.user_id
            WHERE users.role = 'AT'
        """)
        injury_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        injury_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('coach_view_injury.html', injury_records=injury_records)
