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

    if not artist_id:
        flash("User not logged in.", "danger")
        return render_template('artist_settings.html', artist_info=None)

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # 获取完整的用户信息，包含 Middle Name、Age、Gender
        cursor.execute("""
            SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date,
                   address, emergency_contact_name, emergency_contact_phone
            FROM users WHERE user_id = %s
        """, (artist_id,))
        artist_info = cursor.fetchone()

        # 处理 None 值，避免模板渲染时报错
        if artist_info:
            artist_info['middle_name'] = artist_info.get('middle_name', 'N/A')
            artist_info['age'] = artist_info.get('age', 'N/A')
            artist_info['gender'] = artist_info.get('gender', 'N/A')
            artist_info['address'] = artist_info.get('address', 'N/A')
            artist_info['emergency_contact_name'] = artist_info.get('emergency_contact_name', 'N/A')
            artist_info['emergency_contact_phone'] = artist_info.get('emergency_contact_phone', 'N/A')
        else:
            flash("User profile not found.", "danger")

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        artist_info = None
    finally:
        cursor.close()
        cnx.close()

    return render_template('artist_settings.html', artist_info=artist_info)
