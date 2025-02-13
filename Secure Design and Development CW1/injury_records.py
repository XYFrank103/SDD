from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

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

if __name__ == "__main__":
    app.run(debug=True)
