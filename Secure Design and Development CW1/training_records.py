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

if __name__ == "__main__":
    app.run(debug=True)
