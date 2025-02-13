from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        middle_name = request.form.get('middle_name', '').strip()
        last_name = request.form['last_name'].strip()
        role = request.form['role']
        email = request.form['email'].strip()
        age = int(request.form['age'])
        gender = request.form['gender']
        address = request.form.get('address', '').strip()
        emergency_contact_name = request.form.get('emergency_contact_name', '').strip()
        emergency_contact_phone = request.form.get('emergency_contact_phone', '').strip()
        password = request.form['password']

        if age < 7 or age > 70:
            flash('Age must be between 7 and 70.', 'danger')
            return redirect(url_for('add_user'))

        if 7 <= age <= 12 and (not emergency_contact_name or not emergency_contact_phone):
            flash('For users aged 7-12, emergency contact name and phone are required.', 'danger')
            return redirect(url_for('add_user'))

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()

            cursor.execute(f"SELECT MAX(role_id) FROM users WHERE role = '{role}'")
            result = cursor.fetchone()[0]
            role_id = 1 if result is None else result + 1
            user_id = f"{role}{role_id:03}"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute(
                """
                INSERT INTO users (user_id, first_name, middle_name, last_name, role, role_id, password, email, age, gender, join_date, address, emergency_contact_name, emergency_contact_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), %s, %s, %s)
                """,
                (user_id, first_name, middle_name, last_name, role, role_id, hashed_password, email, age, gender, address, emergency_contact_name, emergency_contact_phone)
            )

            cnx.commit()
            flash(f"User {user_id} added successfully!", 'success')

        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')

        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('add_user'))

    return render_template('add_user.html')

if __name__ == "__main__":
    app.run(debug=True)
