from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector

director_performance_records_bp = Blueprint('director_performance_records', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_performance_records_bp.route('/director_performance_records', methods=['GET', 'POST'])
def director_performance_records():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        if request.method == 'POST':
            artist_id = request.form['artist_id']
            performance_date = request.form['performance_date']
            location = request.form['location']
            remarks = request.form['remarks']
            director_id = session.get('user_id')

            if artist_id and performance_date and location and director_id:
                cursor.execute("""
                    INSERT INTO performances (artist_id, director_id, performance_date, location, remarks)
                    VALUES (%s, %s, %s, %s, %s)
                """, (artist_id, director_id, performance_date, location, remarks))
                cnx.commit()
                flash('Performance record added successfully.', 'success')
            else:
                flash('All fields are required to add a performance record.', 'danger')

        cursor.execute("SELECT * FROM performances")
        performance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        performance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_performance_records.html', performance_records=performance_records)

@director_performance_records_bp.route('/delete_director_performance', methods=['POST'])
def delete_director_performance():
    performance_id = request.form['performance_id']
    director_id = session.get('user_id')

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT * FROM performances WHERE id = %s AND director_id = %s
        """, (performance_id, director_id))
        performance = cursor.fetchone()

        if performance:
            cursor.execute("DELETE FROM performances WHERE id = %s", (performance_id,))
            cnx.commit()
            flash('Performance record deleted successfully.', 'success')
        else:
            flash('You can only delete your own performance records.', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('director_performance_records.director_performance_records'))
