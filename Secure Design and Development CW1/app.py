from flask import Flask, render_template, request, redirect, url_for, flash, session
from view_users import view_users, delete_user
from add_remarks import add_remarks
from admin_settings import admin_settings
from settings import settings_bp
from user_attendance import user_attendance
from coach_view_performance import coach_view_performance
from coach_training_records import coach_training_records, delete_coach_training
from coach_view_injury import coach_view_injury_bp
from coach_view_user import coach_view_user_bp
from coach_view_remarks import coach_view_remarks_bp
from coach_add_remarks import coach_add_remarks_bp
from director_performance_records import director_performance_records_bp
from director_view_training import director_view_training_bp
from director_view_attendance import director_view_attendance_bp
from director_view_injury import director_view_injury_bp
from director_view_users import director_view_users_bp
from director_view_remarks import director_view_remarks_bp
from director_add_remarks import director_add_remarks_bp
from director_settings import director_settings_bp
from artist_view_attendance import artist_view_attendance_bp
from artist_view_performance import artist_view_performance_bp
from artist_view_training import artist_view_training_bp
from artist_view_injury import artist_view_injury_bp
from artist_view_remarks import artist_view_remarks_bp
from artist_settings import artist_settings_bp
from director_change_password import director_change_password_bp
from coach_change_password import coach_change_password_bp
from artist_change_password import artist_change_password_bp
from view_users import view_users_bp
from admin_change_password import admin_change_password_bp
import mysql.connector
import bcrypt
import requests
import os
import logging

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

LOG_FOLDER = 'Log'
LOG_FILE = os.path.join(LOG_FOLDER, 'Log.txt')
os.makedirs(LOG_FOLDER, exist_ok=True)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("Unhandled Exception", exc_info=True)
    return render_template('error.html'), 500 

@app.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings_route():
    return admin_settings()

@app.route('/user_attendance', methods=['GET'])
def user_attendance_route():
    return user_attendance()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        recaptcha_response = request.form.get('g-recaptcha-response')

        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': '6Lcn14kqAAAAABoIKoIrSz7-ECxntzmF09T4wCTR',
            'response': recaptcha_response
        }
        recaptcha_result = requests.post(recaptcha_verify_url, data=payload).json()

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (username,))
            user = cursor.fetchone()

            if not recaptcha_result.get('success') or not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                error_message = 'Username or password is incorrect or empty, or Google verification failed.'
            else:
                session['user_id'] = user['user_id']
                session['role'] = user['role']
                role = user['role']

                if role == 'Admin':
                    return redirect(url_for('admin_homepage'))
                elif role == 'AT':
                    return redirect(url_for('artist_homepage'))
                elif role == 'CH':
                    return redirect(url_for('coach_homepage'))
                elif role == 'DR':
                    return redirect(url_for('director_homepage'))

        except mysql.connector.Error as err:
            error_message = f"Error: {err}"
        finally:
            cursor.close()
            cnx.close()

    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin_homepage')
def admin_homepage():
    return render_template('admin_homepage.html')

@app.route('/artist_homepage')
def artist_homepage():
    return render_template('artist_homepage.html')

@app.route('/coach_homepage')
def coach_homepage():
    return render_template('coach_homepage.html')

@app.route('/director_homepage')
def director_homepage():
    return render_template('director_homepage.html')

@app.route('/attendance_records', methods=['GET', 'POST'])
def attendance_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            user_id = request.form['user_id']

            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                flash('No user found with the given User ID.', 'danger')
            else:
                cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND attendance_date = CURDATE()", (user_id,))
                attendance = cursor.fetchone()
                if attendance:
                    flash('Attendance for this user has already been recorded today.', 'warning')
                else:
                    cursor.execute("INSERT INTO attendance (user_id, attendance_date) VALUES (%s, CURDATE())", (user_id,))
                    cnx.commit()
                    flash('Attendance record added successfully.', 'success')

        cursor.execute("SELECT * FROM attendance")
        attendance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        attendance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('attendance_records.html', attendance_records=attendance_records)

@app.route('/delete_attendance', methods=['POST'])
def delete_attendance():
    attendance_id = request.form['attendance_id']
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("DELETE FROM attendance WHERE id = %s", (attendance_id,))
        cnx.commit()
        flash('Attendance record deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('attendance_records'))

@app.route('/performance_records', methods=['GET', 'POST'])
def performance_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            artist_id = request.form['artist_id']
            director_id = request.form['director_id']
            performance_date = request.form['performance_date']
            location = request.form['location']
            remarks = request.form['remarks']

            cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'AT'", (artist_id,))
            artist = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'DR'", (director_id,))
            director = cursor.fetchone()

            if not artist:
                flash('No artist found with the given Artist ID.', 'danger')
            elif not director:
                flash('No director found with the given Director ID.', 'danger')
            else:
                cursor.execute("INSERT INTO performances (artist_id, director_id, performance_date, location, remarks) VALUES (%s, %s, %s, %s, %s)",
                               (artist_id, director_id, performance_date, location, remarks))
                cnx.commit()
                flash('Performance record added successfully.', 'success')

        cursor.execute("SELECT * FROM performances")
        performance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        performance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('performance_records.html', performance_records=performance_records)

@app.route('/delete_performance', methods=['POST'])
def delete_performance():
    performance_id = request.form['performance_id']
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("DELETE FROM performances WHERE id = %s", (performance_id,))
        cnx.commit()
        flash('Performance record deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('performance_records'))

@app.route('/training_records', methods=['GET', 'POST'])
def training_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            artist_id = request.form.get('artist_id', '').strip()
            coach_id = request.form.get('coach_id', '').strip()
            training_date = request.form.get('training_date', '').strip()
            remarks = request.form.get('remarks', '').strip()

            if not artist_id:
                flash('Artist ID cannot be empty.', 'danger')
            if not coach_id:
                flash('Coach ID cannot be empty.', 'danger')
            if not training_date:
                flash('Training Date cannot be empty.', 'danger')

            if artist_id and coach_id and training_date:
                cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'AT'", (artist_id,))
                artist = cursor.fetchone()
                cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'CH'", (coach_id,))
                coach = cursor.fetchone()

                if not artist:
                    flash('No artist found with the given Artist ID.', 'danger')
                elif not coach:
                    flash('No coach found with the given Coach ID.', 'danger')
                else:
                    cursor.execute(
                        "INSERT INTO training (artist_id, coach_id, training_date, remarks) VALUES (%s, %s, %s, %s)",
                        (artist_id, coach_id, training_date, remarks)
                    )
                    cnx.commit()
                    flash('Training record added successfully.', 'success')

        cursor.execute("SELECT * FROM training")
        training_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        training_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('training_records.html', training_records=training_records)

@app.route('/delete_training', methods=['POST'])
def delete_training():
    training_id = request.form['training_id']
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("DELETE FROM training WHERE id = %s", (training_id,))
        cnx.commit()
        flash('Training record deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('training_records'))

@app.route('/injury_records', methods=['GET', 'POST'])
def injury_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            user_id = request.form.get('user_id', '').strip()
            injury_date = request.form.get('injury_date', '').strip()

            if not user_id:
                flash('User ID cannot be empty.', 'danger')
            if not injury_date:
                flash('Injury Date cannot be empty.', 'danger')

            if user_id and injury_date:
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                if not user:
                    flash('No user found with the given User ID.', 'danger')
                else:
                    cursor.execute(
                        "INSERT INTO injuries (user_id, injury_date) VALUES (%s, %s)",
                        (user_id, injury_date)
                    )
                    cnx.commit()
                    flash('Injury record added successfully.', 'success')

        cursor.execute("SELECT * FROM injuries")
        injury_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        injury_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('injury_records.html', injury_records=injury_records)

@app.route('/delete_injury', methods=['POST'])
def delete_injury():
    injury_id = request.form['injury_id']
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("DELETE FROM injuries WHERE id = %s", (injury_id,))
        cnx.commit()
        flash('Injury record deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('injury_records'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        from add_user import add_user
        return add_user()
    return render_template('add_user.html')

app.register_blueprint(coach_view_user_bp)
app.register_blueprint(coach_view_injury_bp)
app.register_blueprint(coach_view_remarks_bp)
app.register_blueprint(coach_add_remarks_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(director_performance_records_bp)
app.register_blueprint(director_view_training_bp)
app.register_blueprint(director_view_attendance_bp)
app.register_blueprint(director_view_injury_bp)
app.register_blueprint(director_view_users_bp)
app.register_blueprint(director_view_remarks_bp)
app.register_blueprint(director_add_remarks_bp, url_prefix="/director_add_remarks")
app.register_blueprint(director_settings_bp)
app.register_blueprint(artist_view_attendance_bp)
app.register_blueprint(artist_view_performance_bp)
app.register_blueprint(artist_view_training_bp)
app.register_blueprint(artist_view_injury_bp)
app.register_blueprint(artist_view_remarks_bp)
app.register_blueprint(artist_settings_bp)
app.register_blueprint(director_change_password_bp)
app.register_blueprint(coach_change_password_bp)
app.register_blueprint(artist_change_password_bp)
app.register_blueprint(view_users_bp)
app.register_blueprint(admin_change_password_bp)

app.add_url_rule('/view_users', view_func=view_users, methods=['GET'])
app.add_url_rule('/delete_user', view_func=delete_user, methods=['POST'])
app.add_url_rule('/add_remarks', view_func=add_remarks, methods=['GET', 'POST'])
app.add_url_rule('/coach_training_records', view_func=coach_training_records, methods=['GET', 'POST'])
app.add_url_rule('/delete_coach_training', view_func=delete_coach_training, methods=['POST'])
app.add_url_rule('/coach_view_performance', view_func=coach_view_performance, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)
