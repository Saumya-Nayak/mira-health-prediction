from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests
import os
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    haemoglobin = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

def get_ai_prediction(glucose, haemoglobin, cholesterol):
    prompt = (
        f"Patient blood test results - Glucose: {glucose} mg/dL, "
        f"Haemoglobin: {haemoglobin} g/dL, Cholesterol: {cholesterol} mg/dL. "
        f"Give a 2-3 sentence health risk assessment. "
        f"Mention possible conditions and brief advice. "
        f"Plain text only, no bullet points, no markdown, no bold symbols."
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "MIRA Health App"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()
        if "choices" not in result:
            return "AI assessment currently unavailable."
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "AI assessment currently unavailable."

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_future_date(dob):
    from datetime import date, datetime
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        return dob_date > date.today()
    except ValueError:
        return True

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        dob = request.form['dob']
        email = request.form['email'].strip()
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        if not full_name or not dob or not email or not glucose or not haemoglobin or not cholesterol:
            flash('All fields are required.', 'danger')
            return render_template('add.html')

        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('add.html')

        if is_future_date(dob):
            flash('Date of birth cannot be a future date.', 'danger')
            return render_template('add.html')

        try:
            glucose = float(glucose)
            haemoglobin = float(haemoglobin)
            cholesterol = float(cholesterol)
        except ValueError:
            flash('Glucose, Haemoglobin, and Cholesterol must be numeric values.', 'danger')
            return render_template('add.html')

        remarks = get_ai_prediction(glucose, haemoglobin, cholesterol)

        patient = Patient(
            full_name=full_name,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient record added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        dob = request.form['dob']
        email = request.form['email'].strip()
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        if not full_name or not dob or not email or not glucose or not haemoglobin or not cholesterol:
            flash('All fields are required.', 'danger')
            return render_template('edit.html', patient=patient)

        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('edit.html', patient=patient)

        if is_future_date(dob):
            flash('Date of birth cannot be a future date.', 'danger')
            return render_template('edit.html', patient=patient)

        try:
            glucose = float(glucose)
            haemoglobin = float(haemoglobin)
            cholesterol = float(cholesterol)
        except ValueError:
            flash('Glucose, Haemoglobin, and Cholesterol must be numeric values.', 'danger')
            return render_template('edit.html', patient=patient)

        remarks = get_ai_prediction(glucose, haemoglobin, cholesterol)

        patient.full_name = full_name
        patient.dob = dob
        patient.email = email
        patient.glucose = glucose
        patient.haemoglobin = haemoglobin
        patient.cholesterol = cholesterol
        patient.remarks = remarks

        db.session.commit()
        flash('Patient record updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', patient=patient)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient record deleted.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)