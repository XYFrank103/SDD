from flask import Blueprint, render_template, session, flash
import mysql.connector

settings_bp = Blueprint('settings', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@settings_bp.route('/settings', methods=['GET'])
def settings():
    user_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, first_name, last_name, role, address, emergency_contact_name, emergency_contact_phone, 
                   join_date, email 
            FROM users 
            WHERE user_id = %s
        """, (user_id,))
        user_info = cursor.fetchone()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        user_info = None
    finally:
        cursor.close()
        cnx.close()

    return render_template('settings.html', user_info=user_info)
