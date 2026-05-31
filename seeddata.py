from app import app, db, Patient

sample_patients = [
    {
        "full_name": "Arjun Mehta",
        "dob": "1990-03-15",
        "email": "arjun.mehta90@gmail.com",
        "glucose": 182.5,
        "haemoglobin": 11.2,
        "cholesterol": 235.0,
        "remarks": "Elevated glucose levels suggest possible Type 2 diabetes risk; haemoglobin is slightly below normal indicating mild anaemia. Recommend consulting a physician for HbA1c testing and dietary modifications to manage blood sugar and iron intake."
    },
    {
        "full_name": "Priya Sharma",
        "dob": "1995-07-22",
        "email": "priya.sharma95@gmail.com",
        "glucose": 78.0,
        "haemoglobin": 10.5,
        "cholesterol": 175.0,
        "remarks": "Haemoglobin is below the normal range for women, indicating iron deficiency anaemia which may cause fatigue and weakness. Glucose and cholesterol levels are within healthy limits; iron-rich diet and possible supplementation are advised."
    },
    {
        "full_name": "Rohit Verma",
        "dob": "1985-11-08",
        "email": "rohit.verma85@gmail.com",
        "glucose": 105.0,
        "haemoglobin": 13.8,
        "cholesterol": 268.0,
        "remarks": "Cholesterol is significantly elevated and puts the patient at increased risk of cardiovascular disease and arterial blockage. Glucose is in the borderline pre-diabetic range; a low-fat diet, regular exercise, and a lipid panel follow-up are strongly recommended."
    },
    {
        "full_name": "Sneha Iyer",
        "dob": "2000-01-30",
        "email": "sneha.iyer2000@gmail.com",
        "glucose": 88.0,
        "haemoglobin": 12.9,
        "cholesterol": 158.0,
        "remarks": "All three blood markers fall within normal and healthy reference ranges for a young adult female. No immediate health concerns are indicated; maintaining a balanced diet and annual check-ups are recommended to sustain these levels."
    },
    {
        "full_name": "Karan Patel",
        "dob": "1978-05-19",
        "email": "karan.patel78@gmail.com",
        "glucose": 210.0,
        "haemoglobin": 12.0,
        "cholesterol": 290.0,
        "remarks": "Both glucose and cholesterol are critically elevated, suggesting a high risk of diabetes and cardiovascular complications. Haemoglobin is slightly low; immediate medical consultation, medication review, and lifestyle intervention including diet and physical activity are urgently advised."
    }
]

with app.app_context():
    for data in sample_patients:
        existing = Patient.query.filter_by(email=data["email"]).first()
        if not existing:
            patient = Patient(**data)
            db.session.add(patient)
    db.session.commit()
    print("Sample data inserted successfully.")