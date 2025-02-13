from flask import Flask, render_template, request, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'art_group_system_secret_key'

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@app.route('/add_remarks', methods=['GET', 'POST'])
def add_remarks():
    if request.method == 'POST':
        remark_text = request.form.get('remark_text', '').strip()
        author_role = session.get('role', '').strip()
        target_role = request.form.get('target_role', '').strip()

        if not remark_text:
            flash('Remark text cannot be empty.', 'danger')
        if not author_role:
            flash('Author role cannot be empty.', 'danger')
        if not target_role:
            flash('Target role cannot be empty.', 'danger')

        if remark_text and author_role and target_role:
            try:
                cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                cursor.execute("""
                    INSERT INTO remarks (remark_text, author_role, target_role)
                    VALUES (%s, %s, %s)
                """, (remark_text, author_role, target_role))
                cnx.commit()
                flash('Remark added successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f"Error: {err}", 'danger')
            finally:
                cursor.close()
                cnx.close()

    user_remarks = []
    try:
        author_role = session.get('role')
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT remark_text, target_role, created_at FROM remarks WHERE author_role = %s", (author_role,))
        user_remarks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        cursor.close()
        cnx.close()

    return render_template('add_remarks.html', user_remarks=user_remarks)

if __name__ == "__main__":
    app.run(debug=True)
