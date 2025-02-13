from flask import Blueprint, render_template, flash, session
import mysql.connector

artist_view_injury_bp = Blueprint('artist_view_injury', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_view_injury_bp.route('/artist_view_injury', methods=['GET'])
def artist_view_injury():
    artist_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, user_id, injury_date
            FROM injuries
            WHERE user_id = %s
        """, (artist_id,))
        injury_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        injury_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_view_injury.html', injury_records=injury_records)
