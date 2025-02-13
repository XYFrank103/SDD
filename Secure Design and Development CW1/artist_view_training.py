from flask import Blueprint, render_template, flash, session
import mysql.connector

artist_view_training_bp = Blueprint('artist_view_training', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_view_training_bp.route('/artist_view_training', methods=['GET'])
def artist_view_training():
    artist_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, artist_id, coach_id, training_date, remarks
            FROM training
            WHERE artist_id = %s
        """, (artist_id,))
        training_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        training_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_view_training.html', training_records=training_records)
