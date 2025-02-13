from flask import Blueprint, render_template, session, flash
import mysql.connector

artist_settings_bp = Blueprint('artist_settings', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@artist_settings_bp.route('/artist_settings', methods=['GET'])
def artist_settings():
    artist_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, first_name, last_name, role, address, emergency_contact_name, emergency_contact_phone, 
                   join_date, email 
            FROM users 
            WHERE user_id = %s
        """, (artist_id,))
        artist_info = cursor.fetchone()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        artist_info = None
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_settings.html', artist_info=artist_info)
