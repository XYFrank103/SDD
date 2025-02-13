from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector

director_add_remarks_bp = Blueprint('director_add_remarks', __name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

@director_add_remarks_bp.route('/director_add_remarks', methods=['GET', 'POST'])
def director_add_remarks():
    if request.method == 'POST':
        remark_text = request.form['remark_text']
        target_role = 'AT' 
        author_role = session.get('role', 'DR') 

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()

            cursor.execute("""
                INSERT INTO remarks (remark_text, author_role, target_role)
                VALUES (%s, %s, %s)
            """, (remark_text, author_role, target_role))
            cnx.commit()
            flash('Remark sent to Artists successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('director_add_remarks'))

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, remark_text, created_at 
            FROM remarks 
            WHERE author_role = 'DR' AND target_role = 'AT'
        """)
        remarks = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        remarks = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_add_remarks.html', remarks=remarks)
