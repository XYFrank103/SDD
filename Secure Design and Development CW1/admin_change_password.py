from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector
import bcrypt

admin_change_password_bp = Blueprint('admin_change_password_bp', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@admin_change_password_bp.route('/admin_change_password', methods=['GET', 'POST'])
def admin_change_password():
    error_message = ""
    success_message = ""

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        admin_user_id = 'Admin'

        if not current_password or not new_password or not confirm_password:
            error_message = "All fields must be filled out."
        elif new_password == current_password:
            error_message = "The new password cannot be the same as the current password."
        elif new_password != confirm_password:
            error_message = "New passwords do not match."
        else:
            try:
                cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor(dictionary=True)

                cursor.execute("SELECT password FROM users WHERE user_id = %s", (admin_user_id,))
                result = cursor.fetchone()

                if result and bcrypt.checkpw(current_password.encode('utf-8'), result['password'].encode('utf-8')):
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_password, admin_user_id))
                    cnx.commit()
                    success_message = "Password changed successfully."
                    return redirect(url_for('admin_settings_route'))
                else:
                    error_message = "Current password is incorrect."

            except mysql.connector.Error as err:
                error_message = f"Database error: {err}"
            finally:
                cursor.close()
                cnx.close()

    return render_template('admin_change_password.html', error_message=error_message, success_message=success_message)
