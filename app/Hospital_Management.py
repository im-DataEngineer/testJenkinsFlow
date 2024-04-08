from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Patient {self.name}>'

# Define Doctor model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Doctor {self.name}>'

# Define Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=True)

    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

# Routes
@app.route('/')
def index():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    return render_template('index.html', patients=patients, doctors=doctors, appointments=appointments)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    diagnosis = request.form.get('diagnosis')
    if name and age and gender and diagnosis:
        new_patient = Patient(name=name, age=age, gender=gender, diagnosis=diagnosis)
        db.session.add(new_patient)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form.get('name')
    specialization = request.form.get('specialization')
    if name and specialization:
        new_doctor = Doctor(name=name, specialization=specialization)
        db.session.add(new_doctor)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form.get('patient_id')
    doctor_id = request.form.get('doctor_id')
    if patient_id and doctor_id:
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id)
        db.session.add(new_appointment)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_patient/<int:patient_id>', methods=['POST'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.name = request.form.get('name')
    patient.age = request.form.get('age')
    patient.gender = request.form.get('gender')
    patient.diagnosis = request.form.get('diagnosis')
    db.session.commit()
    return redirect(url_for('index'))

# Similarly, add routes for search, delete, and update for doctors and appointments

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)