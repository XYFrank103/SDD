from flask import Flask, render_template, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@app.route('/coach_view_performance', methods=['GET'])
def coach_view_performance():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM performances")
        performance_records = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        performance_records = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('coach_view_performance.html', performance_records=performance_records)

if __name__ == "__main__":
    app.run(debug=True)
