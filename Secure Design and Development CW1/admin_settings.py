from flask import Blueprint, render_template, flash, session
import mysql.connector

admin_settings_bp = Blueprint('admin_settings', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@admin_settings_bp.route('/admin_settings', methods=['GET'])
def admin_settings():
    admin_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date,
                   address, emergency_contact_name, emergency_contact_phone
            FROM users WHERE user_id = %s
        """, (admin_id,))
        admin_info = cursor.fetchone()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        admin_info = {}
    finally:
        cursor.close()
        cnx.close()

    return render_template('admin_settings.html', admin_info=admin_info)
