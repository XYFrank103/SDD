from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector

# 创建 Blueprint
director_add_remarks_bp = Blueprint('director_add_remarks', __name__, url_prefix="/director_add_remarks")

# MySQL 配置
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'art_group_system'
}

# 处理 GET 和 POST 请求
@director_add_remarks_bp.route('/', methods=['GET', 'POST'])
def director_add_remarks():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        if request.method == 'POST':
            remark_text = request.form['remark_text']
            coach_role = session.get('role', 'DR')
            target_role = 'AT'
            
            if remark_text:
                cursor.execute("""
                    INSERT INTO remarks (remark_text, author_role, target_role)
                    VALUES (%s, %s, %s)
                """, (remark_text, coach_role, target_role))
                cnx.commit()
                flash('Remark added successfully.', 'success')
            else:
                flash('Remark text cannot be empty.', 'danger')

        cursor.execute("SELECT remark_text, author_role, created_at FROM remarks WHERE target_role = 'AT'")
        remarks = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        remarks = []
    finally:
        cursor.close()
        cnx.close()

    return render_template('director_add_remarks.html', remarks=remarks)