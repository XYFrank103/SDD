import mysql.connector
from mysql.connector import errorcode
import bcrypt
import pyotp

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}

db_name = 'art_group_system'

tables = {}

tables['users'] = (
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(10) NOT NULL UNIQUE,
        first_name VARCHAR(50) NOT NULL,
        middle_name VARCHAR(50),
        last_name VARCHAR(50) NOT NULL,
        role ENUM('Admin', 'AT', 'CH', 'DR') NOT NULL,
        role_id INT NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        gender ENUM('Male', 'Female', 'Other') NOT NULL,
        join_date DATE NOT NULL,
        address VARCHAR(255),
        emergency_contact_name VARCHAR(100),
        emergency_contact_phone VARCHAR(15),
        totp_secret VARCHAR(32),
        UNIQUE(role, role_id)
    )
    """
)

tables['attendance'] = (
    """
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(10) NOT NULL,
        attendance_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)

tables['performances'] = (
    """
    CREATE TABLE IF NOT EXISTS performances (
        id INT AUTO_INCREMENT PRIMARY KEY,
        artist_id VARCHAR(10) NOT NULL,
        director_id VARCHAR(10) NOT NULL,
        performance_date DATE NOT NULL,
        location VARCHAR(255) NOT NULL,
        remarks TEXT,
        FOREIGN KEY (artist_id) REFERENCES users(user_id),
        FOREIGN KEY (director_id) REFERENCES users(user_id)
    )
    """
)

tables['training'] = (
    """
    CREATE TABLE IF NOT EXISTS training (
        id INT AUTO_INCREMENT PRIMARY KEY,
        artist_id VARCHAR(10) NOT NULL,
        coach_id VARCHAR(10) NOT NULL,
        training_date DATE NOT NULL,
        remarks TEXT,
        FOREIGN KEY (artist_id) REFERENCES users(user_id),
        FOREIGN KEY (coach_id) REFERENCES users(user_id)
    )
    """
)

tables['injuries'] = (
    """
    CREATE TABLE IF NOT EXISTS injuries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(10) NOT NULL,
        injury_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)

tables['remarks'] = (
    """
    CREATE TABLE IF NOT EXISTS remarks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        remark_text TEXT NOT NULL,
        author_role ENUM('Admin', 'CH', 'DR') NOT NULL,
        target_role ENUM('AT', 'CH', 'DR') NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        modified_at DATETIME ON UPDATE CURRENT_TIMESTAMP
    )
    """
)

def create_database(cursor):
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8'"
        )
        print(f"Database `{db_name}` created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_tables(cursor):
    cursor.execute(f"USE {db_name}")
    for table_name in tables:
        table_description = tables[table_name]
        try:
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno != errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Error creating table `{table_name}`: {err}")

if __name__ == "__main__":
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        create_database(cursor)
        create_tables(cursor)

        cursor.execute(f"USE {db_name}")
        default_password = "Admin"
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        totp_secret = pyotp.random_base32() 
        admin_user_id = 'Admin'
        cursor.execute(
            """
            INSERT INTO users (user_id, first_name, last_name, role, role_id, password, age, gender, join_date, totp_secret)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), %s)
            ON DUPLICATE KEY UPDATE user_id = user_id
            """,
            (admin_user_id, 'Admin', 'Admin', 'Admin', 1, hashed_password, 0, 'Other', totp_secret)
        )
        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database `{db_name}` already exists.")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()
