from flask import Blueprint, render_template, flash, session
import mysql.connector

artist_view_performance_bp = Blueprint('artist_view_performance', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_view_performance_bp.route('/artist_view_performance', methods=['GET'])
def artist_view_performance():
    artist_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, artist_id, director_id, performance_date, location, remarks
            FROM performances
            WHERE artist_id = %s
        """, (artist_id,))
        performance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        performance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_view_performance.html', performance_records=performance_records)
