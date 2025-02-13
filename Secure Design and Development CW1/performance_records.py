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

@app.route('/performance_records', methods=['GET', 'POST'])
def performance_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            artist_id = request.form.get('artist_id', '').strip()
            director_id = request.form.get('director_id', '').strip()
            performance_date = request.form.get('performance_date', '').strip()
            location = request.form.get('location', '').strip()
            remarks = request.form.get('remarks', '').strip()

            if not artist_id:
                flash('Artist ID cannot be empty.', 'danger')
            if not director_id:
                flash('Director ID cannot be empty.', 'danger')
            if not performance_date:
                flash('Performance Date cannot be empty.', 'danger')
            if not location:
                flash('Location cannot be empty.', 'danger')

            if artist_id and director_id and performance_date and location:
                cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'AT'", (artist_id,))
                artist = cursor.fetchone()
                cursor.execute("SELECT * FROM users WHERE user_id = %s AND role = 'DR'", (director_id,))
                director = cursor.fetchone()

                if not artist:
                    flash('No artist found with the given Artist ID.', 'danger')
                elif not director:
                    flash('No director found with the given Director ID.', 'danger')
                else:
                    cursor.execute(
                        "INSERT INTO performances (artist_id, director_id, performance_date, location, remarks) VALUES (%s, %s, %s, %s, %s)",
                        (artist_id, director_id, performance_date, location, remarks)
                    )
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

if __name__ == "__main__":
    app.run(debug=True)
