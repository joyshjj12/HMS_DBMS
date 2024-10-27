from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Secret key for session management
app.secret_key = '1234'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'hospital_db_1'

# Initialize MySQL
mysql = MySQL(app)

# Home route
@app.route('/')
def index():
    return redirect(url_for('login'))




# Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
#         account = cursor.fetchone()

#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             session['role'] = account['role']

#             if account['role'] == 'admin':
#                 return redirect(url_for('admin_dashboard'))
#             elif account['role'] == 'doctor':
#                 return redirect(url_for('doctor_dashboard'))
#             elif account['role'] == 'patient':
#                 return redirect(url_for('patient_dashboard'))
#         else:
#             flash('Incorrect username/password!', 'danger')
#             return redirect(url_for('login'))

#     return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']  # This is user_id
            session['username'] = account['username']
            session['role'] = account['role']

            # If user is a patient, retrieve and store patient_id
            if account['role'] == 'patient':
                cursor.execute('SELECT id FROM patients WHERE user_id = %s', (account['id'],))
                patient = cursor.fetchone()
                session['patient_id'] = patient['id'] if patient else None

            # If user is a doctor, retrieve and store doctor_id
            elif account['role'] == 'doctor':
                cursor.execute('SELECT id, user_id FROM doctors WHERE user_id = %s', (account['id'],))
                doctor = cursor.fetchone()
                session['doctor_id'] = doctor['id'] if doctor else None  # Store the doctor ID in the session

            # Redirect to the appropriate dashboard
            if account['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif account['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif account['role'] == 'patient':
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Incorrect username/password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# # Sign-Up route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role = request.form['role']  # Role can be 'patient' or 'doctor'

#         cursor = mysql.connection.cursor()
#         try:
#             # Insert into users table
#             cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
#             mysql.connection.commit()

#             # If the role is patient, insert into the patients table
#             if role == 'patient':
#                 patient_name = request.form.get('name')  # Example of getting the patient's name
#                 patient_age = request.form.get('age')    # Example of getting the patient's age
#                 patient_contact = request.form.get('contact')  # Example of getting the patient's contact info

#                 # Insert into patients table
#                 cursor.execute('INSERT INTO patients (name, age, contact_info) VALUES (%s, %s, %s)', (patient_name, patient_age, patient_contact))
#                 mysql.connection.commit()

#             # If the role is doctor, insert into the doctors table
#             elif role == 'doctor':
#                 doctor_name = request.form.get('name')  # Example of getting the doctor's name
#                 specialization = request.form.get('specialization')  # Example of getting doctor's specialization
#                 contact_info = request.form.get('contact')  # Example of getting the doctor's contact info

#                 # Insert into doctors table
#                 cursor.execute('INSERT INTO doctors (name, specialization, contact_info) VALUES (%s, %s, %s)', (doctor_name, specialization, contact_info))
#                 mysql.connection.commit()

#             flash('Sign-up successful! You can now log in.', 'success')
#             return redirect(url_for('login'))
#         except Exception as e:
#             mysql.connection.rollback()  # Roll back in case of error
#             flash('Error: ' + str(e), 'danger')
#             return redirect(url_for('signup'))

#     return render_template('sign_up.html')
# Sign-Up route
# Sign-Up route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role = request.form['role']  # Role can be 'patient' or 'doctor'

#         cursor = mysql.connection.cursor()
#         try:
#             # Insert into users table
#             cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
#             mysql.connection.commit()

#             # Get the last inserted user id
#             user_id = cursor.lastrowid

#             # If the role is patient, insert into the patients table
#             if role == 'patient':
#                 patient_name = request.form.get('name')  # Getting the patient's name
#                 patient_contact = request.form.get('contact')  # Getting the patient's contact info

#                 # Insert into patients table with the user_id
#                 cursor.execute('INSERT INTO patients (name, contact_info, user_id) VALUES (%s, %s, %s)', (patient_name, patient_contact, user_id))
#                 mysql.connection.commit()

#             # If the role is doctor, insert into the doctors table
#             elif role == 'doctor':
#                 doctor_name = request.form.get('name')  # Getting the doctor's name
#                 specialization = request.form.get('specialization')  # Getting doctor's specialization
#                 contact_info = request.form.get('contact')  # Getting the doctor's contact info

#                 # Insert into doctors table with the user_id
#                 cursor.execute('INSERT INTO doctors (name, specialty, contact_info) VALUES (%s, %s, %s)', (doctor_name, specialization, contact_info))
#                 mysql.connection.commit()

#             flash('Sign-up successful! You can now log in.', 'success')
#             return redirect(url_for('login'))
#         except Exception as e:
#             mysql.connection.rollback()  # Roll back in case of error
#             flash('Error: ' + str(e), 'danger')
#             return redirect(url_for('signup'))

#     return render_template('sign_up.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # Ensure you have a field to select role (patient/doctor)
        
        # Example: Assuming you have a users table to store the new user's info
        try:
            # Insert the user into the users table
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
            mysql.connection.commit()
            
            # Get the user_id of the newly created user
            user_id = cursor.lastrowid
            
            # If the role is patient, insert into patients table
            if role == 'patient':
                patient_name = request.form.get('name')  # Getting the patient's name
                patient_contact = request.form.get('contact')  # Getting the patient's contact info

                # Insert into patients table with the user_id
                cursor.execute('INSERT INTO patients (name, contact_info, user_id) VALUES (%s, %s, %s)', (patient_name, patient_contact, user_id))
                mysql.connection.commit()

            # If the role is doctor, insert into the doctors table
            elif role == 'doctor':
                doctor_name = request.form.get('name')  # Getting the doctor's name
                specialization = request.form.get('specialization')  # Getting doctor's specialization
                contact_info = request.form.get('contact')  # Getting the doctor's contact info

                # Insert into doctors table with the user_id
                cursor.execute('INSERT INTO doctors (name, specialty, contact_info, user_id) VALUES (%s, %s, %s, %s)', (doctor_name, specialization, contact_info, user_id))
                mysql.connection.commit()

            flash('Sign-up successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()  # Roll back in case of error
            flash('Error: ' + str(e), 'danger')
            return redirect(url_for('signup'))

    return render_template('sign_up.html')





# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Fetch all doctors
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()
        # Fetch all patients
        cursor.execute('SELECT * FROM patients')
        patients = cursor.fetchall()
        # Fetch all appointments
        cursor.execute('SELECT appointments.id, doctors.name AS doctor, patients.name AS patient, appointments.appointment_date FROM appointments JOIN doctors ON appointments.doctor_id = doctors.id JOIN patients ON appointments.patient_id = patients.id')
        appointments = cursor.fetchall()
        # Fetch all sessions
        cursor.execute('SELECT sessions.id, doctors.name AS doctor, sessions.session_date FROM sessions JOIN doctors ON sessions.doctor_id = doctors.id')
        sessions = cursor.fetchall()
        return render_template('admin_dashboard.html', doctors=doctors, patients=patients, appointments=appointments, sessions=sessions)
    return redirect(url_for('login'))

# Admin - Add doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            specialty = request.form['specialty']
            contact = request.form['contact']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO doctors (name, specialty, contact_info) VALUES (%s, %s, %s)', (name, specialty, contact))
            mysql.connection.commit()

            # Optionally, add to users table for login
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (name.lower(), 'password123', 'doctor'))
            mysql.connection.commit()

            flash('Doctor added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_doctor.html')
    return redirect(url_for('login'))

# Admin - Edit doctor
@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE id = %s', [id])
        doctor = cursor.fetchone()

        if request.method == 'POST':
            name = request.form['name']
            specialty = request.form['specialty']
            contact = request.form['contact']

            cursor.execute('UPDATE doctors SET name = %s, specialty = %s, contact_info = %s WHERE id = %s', (name, specialty, contact, id))
            mysql.connection.commit()

            flash('Doctor updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('edit_doctor.html', doctor=doctor)
    return redirect(url_for('login'))

# Admin - Delete doctor
@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = %s', [id])
        mysql.connection.commit()

        # Also delete from users table if linked
        cursor.execute('DELETE FROM users WHERE username = (SELECT LOWER(name) FROM doctors WHERE id = %s)', [id])
        mysql.connection.commit()

        flash('Doctor deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# Admin - Schedule session
@app.route('/schedule_session', methods=['GET', 'POST'])
def schedule_session():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()

        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            session_date = request.form['session_date']

            cursor.execute('INSERT INTO sessions (doctor_id, session_date) VALUES (%s, %s)', (doctor_id, session_date))
            mysql.connection.commit()

            flash('Session scheduled successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('schedule_session.html', doctors=doctors)
    return redirect(url_for('login'))

# Admin - Remove session
@app.route('/remove_session/<int:id>')
def remove_session(id):
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM sessions WHERE id = %s', [id])
        mysql.connection.commit()

        flash('Session removed successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))




@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'loggedin' in session and session['role'] == 'doctor':
        doctor_id = session.get('doctor_id')  # Use .get() to avoid KeyError
        if doctor_id is None:
            flash('Doctor ID not found in session. Please log in again.', 'danger')
            return redirect(url_for('login'))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Fetch appointments for the logged-in doctor
        # Fetch appointments for the logged-in doctor
        cursor.execute(''' 
            SELECT appointments.id, patients.id AS patient_id, patients.name AS patient, appointments.appointment_date
            FROM appointments
            JOIN patients ON appointments.patient_id = patients.id
            WHERE appointments.doctor_id = %s
        ''', [doctor_id])
        appointments = cursor.fetchall()


        print("Appointments:", appointments)  # Debugging line


        # Fetch sessions for the logged-in doctor
        cursor.execute('SELECT * FROM sessions WHERE doctor_id = %s', [doctor_id])
        sessions = cursor.fetchall()

        return render_template('doctor_dashboard.html', appointments=appointments, sessions=sessions)
    
    return redirect(url_for('login'))




# Doctor - View patient details
@app.route('/doctor/view_patient/<int:patient_id>')
def doctor_view_patient(patient_id):
    if 'loggedin' in session and session['role'] == 'doctor':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patients WHERE id = %s', [patient_id])
        patient = cursor.fetchone()
        return render_template('doctor_view_patient.html', patient=patient)
    
    return redirect(url_for('login'))

# Doctor - Edit account
# @app.route('/edit_doctor', methods=['GET', 'POST'])
# def doctor_edit_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         doctor_id = session['id']
#         cursor.execute('SELECT * FROM doctors WHERE id = %s', [doctor_id])
#         doctor = cursor.fetchone()

#         if request.method == 'POST':
#             name = request.form['name']
#             specialty = request.form['specialty']
#             contact = request.form['contact']
#             password = request.form['password']

#             cursor.execute('''
#                 UPDATE doctors 
#                 SET name = %s, specialty = %s, contact_info = %s 
#                 WHERE id = %s
#             ''', (name, specialty, contact, doctor_id))
#             mysql.connection.commit()

#             # Update password in users table
#             cursor.execute('UPDATE users SET password = %s WHERE username = %s', (password, name.lower()))
#             mysql.connection.commit()

#             flash('Account updated successfully!', 'success')
#             return redirect(url_for('doctor_dashboard'))

#         return render_template('edit_doctor.html', doctor=doctor)
    
#     return redirect(url_for('login'))




# @app.route('/edit_doctor', methods=['GET', 'POST'])
# def doctor_edit_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         doctor_id = session.get('doctor_id')  # Use doctor_id key consistently
#         if doctor_id is None:
#             flash('Doctor ID not found in session. Please log in again.', 'danger')
#             return redirect(url_for('login'))

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM doctors WHERE id = %s', [doctor_id])
#         doctor = cursor.fetchone()

#         if request.method == 'POST':
#             name = request.form['name']
#             specialty = request.form['specialty']
#             contact = request.form['contact']
#             username = request.form['username']  # New field for username
#             password = request.form['password']  # Storing plain text password

#             # Update doctor details in doctors table
#             cursor.execute('''
#                 UPDATE doctors 
#                 SET name = %s, specialty = %s, contact_info = %s 
#                 WHERE id = %s
#             ''', (name, specialty, contact, doctor_id))
#             mysql.connection.commit()

#             # Update username and password in users table
#             cursor.execute('UPDATE users SET username = %s, password = %s WHERE id = %s', 
#                            (username, password, doctor_id))
#             mysql.connection.commit()

#             flash('Account updated successfully!', 'success')
#             return redirect(url_for('doctor_dashboard'))

#         return render_template('edit_doctor.html', doctor=doctor)

#     return redirect(url_for('login'))




@app.route('/doctor_edit_account', methods=['GET', 'POST'])
def doctor_edit_account():
    if 'loggedin' in session and session['role'] == 'doctor':
        doctor_id = session.get('id')  
        if doctor_id is None:
            flash('Doctor ID not found in session. Please log in again.', 'danger')
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE id = %s', [doctor_id])
        doctor = cursor.fetchone()

        if request.method == 'POST':
            name = request.form['name']
            specialty = request.form['specialty']
            contact = request.form['contact']
            username = request.form['username']
            password = request.form['password']

            print(f"Received data: Name: {name}, Specialty: {specialty}, Contact: {contact}, Username: {username}, Password: {password}") 

            try:
                print(f"Updating doctor with ID: {doctor_id}")
                cursor.execute(''' 
                    UPDATE doctors 
                    SET name = %s, specialty = %s, contact_info = %s 
                    WHERE id = %s
                ''', (name, specialty, contact, doctor_id))
                mysql.connection.commit()

                if cursor.rowcount == 0:
                    print("No rows updated in doctors table. Please check the doctor_id.")
                else:
                    print(f"Rows affected for doctor update: {cursor.rowcount}")

                print(f"Updating users with ID: {doctor_id}")
                cursor.execute('UPDATE users SET username = %s, password = %s WHERE id = %s', 
                               (username, password, doctor_id))
                mysql.connection.commit()

                if cursor.rowcount == 0:
                    print("No rows updated in users table. Please check the doctor_id.")
                else:
                    print(f"Rows affected for user update: {cursor.rowcount}")

                flash('Account updated successfully!', 'success')
                return redirect(url_for('doctor_dashboard'))

            except MySQLdb.Error as e:
                mysql.connection.rollback()
                flash(f'Error updating account: {str(e)}', 'danger')
                print(f"Error occurred: {str(e)}")

        return render_template('edit_doctor.html', doctor=doctor)

    return redirect(url_for('login'))



# @app.route('/doctor_edit_account', methods=['GET', 'POST'])
# def doctor_edit_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         doctor_id = session.get('doctor_id')  # Use doctor_id key consistently
#         if doctor_id is None:
#             flash('Doctor ID not found in session. Please log in again.', 'danger')
#             return redirect(url_for('login'))

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM doctors WHERE id = %s', [doctor_id])
#         doctor = cursor.fetchone()

#         if request.method == 'POST':
#             name = request.form['name']
#             specialty = request.form['specialty']
#             contact = request.form['contact']
#             username = request.form['username']  # New field for username
#             password = request.form['password']  # Storing plain text password
            
#             print(f"Doctor ID: {doctor_id}")
#             print(f"Received data: Name: {name}, Specialty: {specialty}, Contact: {contact}, Username: {username}, Password: {password}")


#             try:
#                 # Update doctor details in doctors table
#                 cursor.execute(''' 
#                     UPDATE doctors 
#                     SET name = %s, specialty = %s, contact_info = %s 
#                     WHERE id = %s
#                 ''', (name, specialty, contact, doctor_id))
#                 mysql.connection.commit()

#                 # Update username and password in users table
#                 cursor.execute('UPDATE users SET username = %s, password = %s WHERE id = %s', 
#                                (username, password, doctor_id))
#                 mysql.connection.commit()

#                 flash('Account updated successfully!', 'success')
#                 return redirect(url_for('doctor_dashboard'))

#             except MySQLdb.Error as e:
#                 mysql.connection.rollback()  # Rollback in case of error
#                 flash(f'Error updating account: {str(e)}', 'danger')

#         return render_template('edit_doctor.html', doctor=doctor)

#     return redirect(url_for('login'))

@app.route('/doctor_delete_account', methods=['POST'])
def doctor_delete_account():
    if 'loggedin' in session and session['role'] == 'doctor':
        cursor = mysql.connection.cursor()
        doctor_id = session['doctor_id']
        
        # Get user's user_id from the doctors table
        cursor.execute('SELECT user_id FROM doctors WHERE id = %s', [doctor_id])
        result = cursor.fetchone()
        user_id = result[0] if result else None

        try:
            # Delete associated appointments
            cursor.execute('DELETE FROM appointments WHERE doctor_id = %s', [doctor_id])
            mysql.connection.commit()

            # Delete associated sessions
            cursor.execute('DELETE FROM sessions WHERE doctor_id = %s', [doctor_id])
            mysql.connection.commit()

            # Delete from doctors table
            cursor.execute('DELETE FROM doctors WHERE id = %s', [doctor_id])
            mysql.connection.commit()

            # Delete from users table
            if user_id:
                cursor.execute('DELETE FROM users WHERE id = %s', [user_id])
                mysql.connection.commit()

            flash('Account deleted successfully!', 'success')

        except Exception as e:
            mysql.connection.rollback()  # Roll back in case of error
            flash('An error occurred: {}'.format(str(e)), 'error')
        
        finally:
            cursor.close()  # Ensure the cursor is closed
            session.clear()
        
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))



# # Doctor - Delete account
# @app.route('/doctor_delete_account', methods=['POST'])
# def doctor_delete_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         cursor = mysql.connection.cursor()
#         doctor_id = session['id']
        
#         # Get doctor's username
#         cursor.execute('SELECT LOWER(name) AS username FROM doctors WHERE id = %s', [doctor_id])
#         result = cursor.fetchone()
#         username = result[0] if result else None

#         # Delete from doctors table
#         cursor.execute('DELETE FROM doctors WHERE id = %s', [doctor_id])
#         mysql.connection.commit()

#         # Delete from users table
#         if username:
#             cursor.execute('DELETE FROM users WHERE username = %s', [username])
#             mysql.connection.commit()

#         session.clear()
#         flash('Account deleted successfully!', 'success')
#         return redirect(url_for('login'))
    
#     return redirect(url_for('login'))

# Doctor - Approve or Disapprove appointment
@app.route('/doctor/appointment/<int:appointment_id>/action', methods=['POST'])
def doctor_appointment_action(appointment_id):
    if 'loggedin' in session and session['role'] == 'doctor':
        action = request.form.get('action')  # 'approve' or 'disapprove'
        cursor = mysql.connection.cursor()
        
        if action == 'approve':
            cursor.execute('UPDATE appointments SET status = %s WHERE id = %s', ('approved', appointment_id))
            flash('Appointment approved!', 'success')
        elif action == 'disapprove':
            cursor.execute('UPDATE appointments SET status = %s WHERE id = %s', ('disapproved', appointment_id))
            flash('Appointment disapproved!', 'danger')

        mysql.connection.commit()
        return redirect(url_for('doctor_dashboard'))
    
    return redirect(url_for('login'))


# @app.route('/doctor_dashboard')
# def doctor_dashboard():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         doctor_id = session['id']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # Fetch appointments
#         cursor.execute('SELECT appointments.id, patients.name AS patient, appointments.appointment_date FROM appointments JOIN patients ON appointments.patient_id = patients.id WHERE appointments.doctor_id = %s', [doctor_id])
#         appointments = cursor.fetchall()
#         # Fetch sessions
#         cursor.execute('SELECT * FROM sessions WHERE doctor_id = %s', [doctor_id])
#         sessions = cursor.fetchall()
#         return render_template('doctor_dashboard.html', appointments=appointments, sessions=sessions)
#     return redirect(url_for('login'))

# # Doctor - View patient details
# @app.route('/doctor/view_patient/<int:patient_id>')
# def doctor_view_patient(patient_id):
#     if 'loggedin' in session and session['role'] == 'doctor':
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM patients WHERE id = %s', [patient_id])
#         patient = cursor.fetchone()
#         return render_template('doctor_view_patient.html', patient=patient)
#     return redirect(url_for('login'))

# # Doctor - Edit account
# @app.route('/doctor_edit_account', methods=['GET', 'POST'])
# def doctor_edit_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         doctor_id = session['id']
#         cursor.execute('SELECT * FROM doctors WHERE id = %s', [doctor_id])
#         doctor = cursor.fetchone()

#         if request.method == 'POST':
#             name = request.form['name']
#             specialty = request.form['specialty']
#             contact = request.form['contact']
#             password = request.form['password']

#             cursor.execute('UPDATE doctors SET name = %s, specialty = %s, contact_info = %s WHERE id = %s', (name, specialty, contact, doctor_id))
#             mysql.connection.commit()

#             # Update password in users table
#             cursor.execute('UPDATE users SET password = %s WHERE username = %s', (password, name.lower()))
#             mysql.connection.commit()

#             flash('Account updated successfully!', 'success')
#             return redirect(url_for('doctor_dashboard'))

#         return render_template('doctor_edit_account.html', doctor=doctor)
#     return redirect(url_for('login'))

# # Doctor - Delete account
# @app.route('/doctor_delete_account', methods=['POST'])
# def doctor_delete_account():
#     if 'loggedin' in session and session['role'] == 'doctor':
#         cursor = mysql.connection.cursor()
#         doctor_id = session['id']
#         # Get doctor's username
#         cursor.execute('SELECT LOWER(name) AS username FROM doctors WHERE id = %s', [doctor_id])
#         result = cursor.fetchone()
#         username = result[0] if result else None

#         # Delete from doctors table
#         cursor.execute('DELETE FROM doctors WHERE id = %s', [doctor_id])
#         mysql.connection.commit()

#         # Delete from users table
#         if username:
#             cursor.execute('DELETE FROM users WHERE username = %s', [username])
#             mysql.connection.commit()

#         session.clear()
#         flash('Account deleted successfully!', 'success')
#         return redirect(url_for('login'))
#     return redirect(url_for('login'))

######################################
# Patient Routes
######################################

# Patient dashboard
@app.route('/patient_dashboard')
def patient_dashboard():
    if 'loggedin' in session and session['role'] == 'patient':
        patient_id = session['patient_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Fetch appointments
        cursor.execute('SELECT appointments.id, doctors.name AS doctor, appointments.appointment_date FROM appointments JOIN doctors ON appointments.doctor_id = doctors.id WHERE appointments.patient_id = %s', [patient_id])
        appointments = cursor.fetchall()
        return render_template('patient_dashboard.html', appointments=appointments)
    return redirect(url_for('login'))


@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'loggedin' in session and session['role'] == 'patient':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch doctors for the dropdown
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()

        if request.method == 'POST':
            doctor_id = request.form['doctor_id']
            appointment_date = request.form['appointment_date']
            patient_id = session.get('patient_id')  # Get patient_id from session

            # Debugging: Log values
            print(f"Inserting appointment with Doctor ID: {doctor_id}, Patient ID: {patient_id}, Appointment Date: {appointment_date}")

            # Check if the patient exists
            cursor.execute('SELECT * FROM patients WHERE user_id = %s', (session['id'],))  # Get patient based on user_id
            patient = cursor.fetchone()
            if not patient:
                print("Patient does not exist in the database.")
                flash('Error: Patient does not exist.', 'danger')
                return redirect(url_for('patient_dashboard'))

            # Check if the doctor is available on that date (optional)
            # This assumes your appointments table has a way to check for availability
            cursor.execute('SELECT * FROM appointments WHERE doctor_id = %s AND appointment_date = %s', (doctor_id, appointment_date))
            existing_appointments = cursor.fetchall()
            if existing_appointments:
                flash('Error: The doctor is not available on that date.', 'danger')
                return redirect(url_for('book_appointment'))

            # Proceed to insert
            cursor.execute('INSERT INTO appointments (doctor_id, patient_id, appointment_date) VALUES (%s, %s, %s)', 
                           (doctor_id, patient_id, appointment_date))
            mysql.connection.commit()

            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_dashboard'))

        return render_template('book_appointment.html', doctors=doctors)
    
    return redirect(url_for('login'))




# Patient - Edit account
@app.route('/patient_edit_account', methods=['GET', 'POST'])
def patient_edit_account():
    if 'loggedin' in session and session['role'] == 'patient':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        patient_id = session['id']
        cursor.execute('SELECT * FROM patients WHERE id = %s', [patient_id])
        patient = cursor.fetchone()

        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            contact = request.form['contact']
            password = request.form['password']

            cursor.execute('UPDATE patients SET name = %s, age = %s, contact_info = %s WHERE id = %s', (name, age, contact, patient_id))
            mysql.connection.commit()

            # Update password in users table
            cursor.execute('UPDATE users SET password = %s WHERE username = %s', (password, name.lower()))
            mysql.connection.commit()

            flash('Account updated successfully!', 'success')
            return redirect(url_for('patient_dashboard'))

        return render_template('patient_edit_account.html', patient=patient)
    return redirect(url_for('login'))

# Patient - Delete account
# @app.route('/patient_delete_account', methods=['POST'])
# def patient_delete_account():
#     if 'loggedin' in session and session['role'] == 'patient':
#         cursor = mysql.connection.cursor()
#         patient_id = session['patient_id']
#         # Get patient's username
#         cursor.execute('SELECT LOWER(name) AS username FROM patients WHERE id = %s', [patient_id])
#         result = cursor.fetchone()
#         username = result[0] if result else None

#         # Delete from patients table
#         cursor.execute('DELETE FROM patients WHERE id = %s', [patient_id])
#         mysql.connection.commit()

#         # Delete from users table
#         if username:
#             cursor.execute('DELETE FROM users WHERE username = %s', [username])
#             mysql.connection.commit()

#         session.clear()
#         flash('Account deleted successfully!', 'success')
#         return redirect(url_for('login'))
#     return redirect(url_for('login'))

# @app.route('/patient_delete_account', methods=['POST'])
# def patient_delete_account():
#     if 'loggedin' in session and session['role'] == 'patient':
#         cursor = mysql.connection.cursor()
#         user_id = session['id']  # Get the user_id from the session
#         print(f"User ID from session: {user_id}")  # Debugging output

#         # 1. Get the patient_id associated with this user
#         cursor.execute('SELECT id FROM patients WHERE user_id = %s', [user_id])
#         result = cursor.fetchone()

#         if result is None:
#             flash('No patient found with the given user ID.', 'danger')
#             print("No patient found.")  # Debugging output
#             return redirect(url_for('login'))

#         patient_id = result[0]  # Get the patient_id
#         print(f"Patient ID to delete: {patient_id}")  # Debugging output

#         try:
#             # 2. Delete associated appointments
#             cursor.execute('DELETE FROM appointments WHERE patient_id = %s', [patient_id])
#             mysql.connection.commit()
#             print(f"Deleted appointments for patient ID: {patient_id}")  # Debugging output

#             # 3. Delete from patients table
#             cursor.execute('DELETE FROM patients WHERE id = %s', [patient_id])
#             mysql.connection.commit()
#             print(f"Deleted patient with ID: {patient_id}")  # Debugging output

#             # 4. Delete from users table
#             cursor.execute('DELETE FROM users WHERE id = %s', [user_id])
#             mysql.connection.commit()
#             print(f"Deleted user with ID: {user_id}")  # Debugging output

#             flash('Account deleted successfully!', 'success')

#         except Exception as e:
#             mysql.connection.rollback()  # Roll back in case of error
#             flash('An error occurred: {}'.format(str(e)), 'error')
#             print(f"Error occurred: {e}")  # Debugging output

#         finally:
#             cursor.close()  # Ensure the cursor is closed
#             session.clear()  # Clear the session

#         return redirect(url_for('login'))

#     return redirect(url_for('login'))


@app.route('/patient_delete_account', methods=['POST'])
def patient_delete_account():
    if 'loggedin' in session and session['role'] == 'patient':
        cursor = mysql.connection.cursor()
        user_id = session['id']  # Get the user_id from the session
        print(f"User ID from session: {user_id}")  # Debugging output

        # 1. Get the patient_id associated with this user
        cursor.execute('SELECT id FROM patients WHERE user_id = %s', [user_id])
        result = cursor.fetchone()

        if result is None:
            flash('No patient found with the given user ID.', 'danger')
            print("No patient found.")  # Debugging output
            return redirect(url_for('login'))

        patient_id = result[0]  # Get the patient_id
        print(f"Patient ID to delete: {patient_id}")  # Debugging output

        try:
            # 2. Delete associated appointments
            cursor.execute('DELETE FROM appointments WHERE patient_id = %s', [patient_id])
            mysql.connection.commit()
            print(f"Deleted appointments for patient ID: {patient_id}")  # Debugging output

            # 3. Delete from patients table
            cursor.execute('DELETE FROM patients WHERE id = %s', [patient_id])
            mysql.connection.commit()
            print(f"Deleted patient with ID: {patient_id}")  # Debugging output

            # 4. Delete from users table
            cursor.execute('DELETE FROM users WHERE id = %s', [user_id])
            mysql.connection.commit()
            print(f"Deleted user with ID: {user_id}")  # Debugging output

            flash('Account deleted successfully!', 'success')

        except Exception as e:
            mysql.connection.rollback()  # Roll back in case of error
            flash('An error occurred: {}'.format(str(e)), 'error')
            print(f"Error occurred: {e}")  # Debugging output

        finally:
            cursor.close()  # Ensure the cursor is closed
            session.clear()  # Clear the session

        return redirect(url_for('login'))
    
    return redirect(url_for('login'))





######################################
# Run the Flask app
######################################

if __name__ == '__main__':
    app.run(debug=True)
