import os
import sys

# Add the parent directory of the app package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from app.Hospital_Management import app, db, Patient, Doctor, Appointment
class TestHospitalManagementApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.context = app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    @patch('app.Hospital_Management.render_template')
    def test_index_route(self, mock_render_template):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('index.html', patients=[], doctors=[], appointments=[])

    def test_add_patient_route(self):
        response = self.client.post('/add_patient', data={'name': 'John Doe', 'age': 30, 'gender': 'Male', 'diagnosis': 'Fever'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the patient is added to the database
        patient = Patient.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.gender, 'Male')
        self.assertEqual(patient.diagnosis, 'Fever')

    def test_add_doctor_route(self):
        response = self.client.post('/add_doctor', data={'name': 'Dr. Smith', 'specialization': 'Cardiology'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the doctor is added to the database
        doctor = Doctor.query.filter_by(name='Dr. Smith').first()
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.specialization, 'Cardiology')

    def test_add_appointment_route(self):
        # Add a patient and a doctor first
        new_patient = Patient(name='Alice', age=25, gender='Female', diagnosis='Headache')
        db.session.add(new_patient)
        new_doctor = Doctor(name='Dr. Brown', specialization='Neurology')
        db.session.add(new_doctor)
        db.session.commit()

        response = self.client.post('/add_appointment', data={'patient_id': new_patient.id, 'doctor_id': new_doctor.id})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the appointment is added to the database
        appointment = Appointment.query.filter_by(patient_id=new_patient.id, doctor_id=new_doctor.id).first()
        self.assertIsNotNone(appointment)

    def test_delete_patient_route(self):
        # Add a patient first
        new_patient = Patient(name='Jane', age=40, gender='Female', diagnosis='Cold')
        db.session.add(new_patient)
        db.session.commit()

        response = self.client.post(f'/delete_patient/{new_patient.id}')
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the patient is deleted from the database
        deleted_patient = Patient.query.get(new_patient.id)
        self.assertIsNone(deleted_patient)

    def test_update_patient_route(self):
        # Add a patient first
        new_patient = Patient(name='Bob', age=35, gender='Male', diagnosis='Allergy')
        db.session.add(new_patient)
        db.session.commit()

        updated_name = 'Bobby'
        updated_age = 36
        updated_gender = 'Male'
        updated_diagnosis = 'Allergy'

        response = self.client.post(f'/update_patient/{new_patient.id}', data={'name': updated_name, 'age': updated_age, 'gender': updated_gender, 'diagnosis': updated_diagnosis})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the patient is updated in the database
        updated_patient = Patient.query.get(new_patient.id)
        self.assertEqual(updated_patient.name, updated_name)
        self.assertEqual(updated_patient.age, updated_age)
        self.assertEqual(updated_patient.gender, updated_gender)
        self.assertEqual(updated_patient.diagnosis, updated_diagnosis)

if __name__ == '__main__':
    unittest.main()
