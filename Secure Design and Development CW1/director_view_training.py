from flask import Blueprint, render_template, flash
import mysql.connector

director_view_training_bp = Blueprint('director_view_training', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_view_training_bp.route('/director_view_training', methods=['GET'])
def director_view_training():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT training.id, training.artist_id, training.coach_id, training.training_date, training.remarks,
                   artist.first_name AS artist_first_name, artist.last_name AS artist_last_name,
                   coach.first_name AS coach_first_name, coach.last_name AS coach_last_name
            FROM training
            JOIN users AS artist ON training.artist_id = artist.user_id
            JOIN users AS coach ON training.coach_id = coach.user_id
        """)
        training_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        training_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_view_training.html', training_records=training_records)
