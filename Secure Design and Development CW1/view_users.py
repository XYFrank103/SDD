from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
import bcrypt

view_users_bp = Blueprint('view_users', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@view_users_bp.route('/view_users', methods=['GET', 'POST'])
def view_users():
    search_query = request.form.get('search_query', '').strip() if request.method == 'POST' else ''
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        if search_query:
            cursor.execute("""
                SELECT user_id, first_name, middle_name, last_name, role, email, age, gender, join_date, address, 
                       emergency_contact_name, emergency_contact_phone
                FROM users
                WHERE user_id != 'Admin' 
                AND (user_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR role LIKE %s)
            """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        else:
            cursor.execute("""
                SELECT user_id, first_name, middle_name, last_name, role, email, age, gender, join_date, address, 
                       emergency_contact_name, emergency_contact_phone
                FROM users WHERE user_id != 'Admin'
            """)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        users = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('view_users.html', users=users, search_query=search_query)


@view_users_bp.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        if 'reset_password' in request.form:
            try:
                cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()

                default_password = "art@group123"
                hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                cursor.execute("""
                    UPDATE users SET password = %s WHERE user_id = %s
                """, (hashed_password, user_id))
                cnx.commit()
                flash(f"Password for user {user_id} reset successfully!", "success")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
            finally:
                cursor.close()
                cnx.close()

            return redirect(url_for('view_users.view_users'))

        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name') if 'no_middle_name' not in request.form else None
        last_name = request.form['last_name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form.get('address')
        emergency_contact_name = request.form.get('emergency_contact_name') if 'no_emergency_contact_name' not in request.form else None
        emergency_contact_phone = request.form.get('emergency_contact_phone') if 'no_emergency_contact_phone' not in request.form else None

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()

            cursor.execute("""
                UPDATE users 
                SET first_name = %s, middle_name = %s, last_name = %s, email = %s, age = %s, gender = %s, 
                    address = %s, emergency_contact_name = %s, emergency_contact_phone = %s
                WHERE user_id = %s
            """, (first_name, middle_name, last_name, email, age, gender, address, emergency_contact_name,
                  emergency_contact_phone, user_id))
            cnx.commit()
            flash(f"User {user_id} updated successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('view_users.view_users'))

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
        user = None
    finally:
        cursor.close()
        cnx.close()

    return render_template('edit_user.html', user=user)


@view_users_bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')

    if not user_id:
        flash("User ID is missing. Unable to delete.", "danger")
        return redirect(url_for('view_users.view_users'))

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone()[0] == 0:
            flash(f"User {user_id} does not exist.", "danger")
        else:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            cnx.commit()
            flash(f"User {user_id} deleted successfully.", "success")
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('view_users.view_users'))

