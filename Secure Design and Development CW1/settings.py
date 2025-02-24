from flask import Blueprint, render_template, flash, session
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

    if not user_id:
        flash("User not logged in.", "danger")
        return render_template('settings.html', user_info=None)

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # 获取完整的用户信息，包括 Middle Name、Age、Gender
        cursor.execute("""
            SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date,
                   address, emergency_contact_name, emergency_contact_phone
            FROM users WHERE user_id = %s
        """, (user_id,))
        user_info = cursor.fetchone()

        # 处理 None 值，避免模板渲染时报错
        if user_info:
            user_info['middle_name'] = user_info.get('middle_name', 'N/A')
            user_info['age'] = user_info.get('age', 'N/A')
            user_info['gender'] = user_info.get('gender', 'N/A')
            user_info['address'] = user_info.get('address', 'N/A')
            user_info['emergency_contact_name'] = user_info.get('emergency_contact_name', 'N/A')
            user_info['emergency_contact_phone'] = user_info.get('emergency_contact_phone', 'N/A')
        else:
            flash("User profile not found.", "danger")

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        user_info = None
    finally:
        cursor.close()
        cnx.close()

    return render_template('settings.html', user_info=user_info)
