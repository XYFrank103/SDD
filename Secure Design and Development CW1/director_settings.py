from flask import Blueprint, render_template, flash, session
import mysql.connector

director_settings_bp = Blueprint('director_settings', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_settings_bp.route('/director_settings', methods=['GET'])
def director_settings():
    director_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date,
                   address, emergency_contact_name, emergency_contact_phone
            FROM users WHERE user_id = %s
        """, (director_id,))
        director_info = cursor.fetchone()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        director_info = {}
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_settings.html', director_info=director_info)
