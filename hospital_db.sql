CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(255),
    role ENUM('admin', 'doctor', 'patient')
);

CREATE TABLE doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    specialty VARCHAR(100),
    contact_info VARCHAR(100)
);

CREATE TABLE patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    contact_info VARCHAR(100)
);

CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT,
    patient_id INT,
    appointment_date DATE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT,
    session_date DATE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
