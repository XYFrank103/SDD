from flask import Flask, render_template, request, flash, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@app.route('/coach_training_records', methods=['GET', 'POST'])
def coach_training_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        
        if request.method == 'POST':
            artist_id = request.form['artist_id']
            training_date = request.form['training_date']
            remarks = request.form['remarks']
            coach_id = session.get('user_id')

            if artist_id and training_date and coach_id:
                cursor.execute("""
                    INSERT INTO training (artist_id, coach_id, training_date, remarks)
                    VALUES (%s, %s, %s, %s)
                """, (artist_id, coach_id, training_date, remarks))
                cnx.commit()
                flash('Training record added successfully.', 'success')
            else:
                flash('All fields are required to add a training record.', 'danger')

        cursor.execute("SELECT * FROM training")
        training_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        training_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('coach_training_records.html', training_records=training_records)

@app.route('/delete_coach_training', methods=['POST'])
def delete_coach_training():
    training_id = request.form['training_id']
    coach_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT * FROM training WHERE id = %s AND coach_id = %s
        """, (training_id, coach_id))
        training = cursor.fetchone()

        if training:
            cursor.execute("DELETE FROM training WHERE id = %s", (training_id,))
            cnx.commit()
            flash('Training record deleted successfully.', 'success')
        else:
            flash('You can only delete your own training records.', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('coach_training_records'))

if __name__ == "__main__":
    app.run(debug=True)
