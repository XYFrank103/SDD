from flask import Blueprint, render_template, request, flash
import mysql.connector

coach_view_user_bp = Blueprint('coach_view_user', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@coach_view_user_bp.route('/coach_view_user', methods=['GET', 'POST'])
def coach_view_user():
    search_query = request.form.get('search_query', '').strip() if request.method == 'POST' else ''
    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        if search_query:
            cursor.execute("""
                SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date, address, emergency_contact_name, emergency_contact_phone
                FROM users
                WHERE role = 'AT' AND (user_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s)
            """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        else:
            cursor.execute("""
                SELECT user_id, first_name, middle_name, last_name, email, age, gender, join_date, address, emergency_contact_name, emergency_contact_phone
                FROM users WHERE role = 'AT'
            """)
        
        artists = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        artists = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('coach_view_user.html', artists=artists, search_query=search_query)
