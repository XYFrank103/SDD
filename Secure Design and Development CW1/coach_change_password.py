from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
import bcrypt
from otp import send_otp

coach_change_password_bp = Blueprint('coach_change_password_bp', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@coach_change_password_bp.route('/coach_change_password', methods=['GET', 'POST'])
def coach_change_password():
    coach_id = session.get('user_id')
    otp_session = session.get('otp', None)

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        entered_otp = request.form.get('otp')

        if not new_password or not confirm_password or not entered_otp:
            flash("All fields are required, or the passwords/OTP are incorrect.", "danger")
            return render_template('coach_change_password.html')

        if new_password != confirm_password or otp_session is None or entered_otp != otp_session:
            flash("All fields are required, or the passwords/OTP are incorrect.", "danger")
            return render_template('coach_change_password.html')

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor(dictionary=True)

            cursor.execute("SELECT password FROM users WHERE user_id = %s", (coach_id,))
            user = cursor.fetchone()

            if bcrypt.checkpw(new_password.encode('utf-8'), user['password'].encode('utf-8')):
                flash("New password cannot be the same as the old password.", "danger")
                return render_template('coach_change_password.html')
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_password, coach_id))
                cnx.commit()
                return redirect(url_for('settings.settings'))

        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            cursor.close()
            cnx.close()

    return render_template('coach_change_password.html')

@coach_change_password_bp.route('/send_otp', methods=['POST'])
def send_otp_route():
    coach_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT email FROM users WHERE user_id = %s", (coach_id,))
        user = cursor.fetchone()

        if user:
            otp = send_otp(user['email'])
            if otp:
                session['otp'] = otp
                flash("OTP has been sent to your registered email address.", "success")
            else:
                flash("Failed to send OTP. Please try again.", "danger")

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('coach_change_password_bp.coach_change_password'))
