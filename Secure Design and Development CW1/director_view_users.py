from flask import Blueprint, render_template, request, flash
import mysql.connector

director_view_users_bp = Blueprint('director_view_users', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_view_users_bp.route('/director_view_users', methods=['GET', 'POST'])
def director_view_users():
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

    return render_template('director_view_users.html', artists=artists, search_query=search_query)
