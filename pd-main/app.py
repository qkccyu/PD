from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from model import predict

# ---------------------------------------------------------
#  Load environment variables
# ---------------------------------------------------------
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = True

# Folder for uploaded scans
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'scans')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# ---------------------------------------------------------
#  DATABASE MODELS
# ---------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.String(120), default="Not set")
    severity = db.Column(db.String(50), default="Mild")
    last_visit = db.Column(db.String(50), default="Today")

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(200), nullable=True)
    analyzed = db.Column(db.Boolean, default=False)

# ---------------------------------------------------------
#  ROUTES — WEB PAGES
# ---------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Clear any existing session
    session.clear()
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"Login attempt - Username: {username}")  # Debug log
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        if user:
            print("User found in database")  # Debug log
            if user.check_password(password):
                print("Password is correct")  # Debug log
                session.clear()
                session['user_id'] = user.id
                flash('Successfully logged in!', 'success')
                return redirect(url_for('landing'))
            else:
                print("Password is incorrect")  # Debug log
                flash(f'Invalid password for user {username}. Try admin/admin123', 'danger')
        else:
            print("User not found in database")  # Debug log
            flash(f'Username {username} not found. Try admin/admin123', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Username already exists!', 'danger')
        elif email_exists:
            flash('Email already registered!', 'danger')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/patients')
def patients():
    patient_records = Patient.query.all()
    return render_template('patients.html', patient_records=patient_records)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/scan')
def scan():
    # Only show patients that exist in DB for dropdown
    patients = [p.name for p in Patient.query.all()]
    return render_template('scan.html', patients=patients)

@app.route('/medications')
def medications():
    return render_template('medications.html')

@app.route('/predict-ui')
@login_required
def predict_ui():
    return render_template('predict.html')

# ---------------------------------------------------------
#  API ROUTES — PATIENTS
# ---------------------------------------------------------
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "sex": p.sex,
            "condition": p.condition,
            "severity": p.severity,
            "last_visit": p.last_visit
        }
        for p in patients
    ])

@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        sex=data['sex'],
        last_visit="Today",
        condition="Not set",
        severity="Mild"
    )
    db.session.add(new_patient)
    db.session.commit()

    # Return full new record instead of just a message
    return jsonify({
        "id": new_patient.id,
        "name": new_patient.name,
        "age": new_patient.age,
        "sex": new_patient.sex,
        "condition": new_patient.condition,
        "severity": new_patient.severity,
        "last_visit": new_patient.last_visit
    })

@app.route('/api/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.get_json()

    patient.last_visit = data.get('last_visit', patient.last_visit)
    patient.condition = data.get('condition', patient.condition)
    patient.severity = data.get('severity', patient.severity)
    db.session.commit()

    # Return updated patient info
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "sex": patient.sex,
        "condition": patient.condition,
        "severity": patient.severity,
        "last_visit": patient.last_visit
    })

# ✅ Added DELETE route for patients
@app.route('/api/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})

# ---------------------------------------------------------
#  API ROUTES — MEDICATIONS
# ---------------------------------------------------------
@app.route('/api/medications', methods=['GET'])
def get_medications():
    meds = Medication.query.all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "type": m.type,
            "stock": m.stock,
            "image_url": f"/static/uploads/scans/{m.image_filename}" if m.image_filename else None
        }
        for m in meds
    ])

@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    new_med = Medication(
        name=data['name'],
        type=data['type'],
        stock=data['stock']
    )
    db.session.add(new_med)
    db.session.commit()
    return jsonify({
        "id": new_med.id,
        "name": new_med.name,
        "type": new_med.type,
        "stock": new_med.stock,
        "image_url": None
    })

@app.route('/api/medications/<int:id>', methods=['PUT'])
def update_medication(id):
    med = Medication.query.get_or_404(id)
    data = request.get_json()
    med.name = data['name']
    med.type = data['type']
    med.stock = data['stock']
    db.session.commit()
    return jsonify({
        "id": med.id,
        "name": med.name,
        "type": med.type,
        "stock": med.stock
    })

# ✅ Added DELETE route for medications
@app.route('/api/medications/<int:id>', methods=['DELETE'])
def delete_medication(id):
    med = Medication.query.get_or_404(id)
    db.session.delete(med)
    db.session.commit()
    return jsonify({"message": "Medication deleted successfully"})

@app.route('/api/medications/<int:med_id>/image', methods=['POST'])
def upload_medication_image(med_id):
    med = Medication.query.get_or_404(med_id)
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    try:
        file.save(upload_path)
        med.image_filename = filename
        db.session.commit()
        return jsonify({'message': 'Image uploaded successfully'})
    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------
#  API ROUTE — SCANS
# ---------------------------------------------------------
@app.route('/api/scans', methods=['POST'])
def save_scan():
    patient_name = request.form.get('patient_name')
    notes = request.form.get('notes')
    image = request.files.get('image')

    if not patient_name or not image:
        return jsonify({'error': 'Missing patient name or image'}), 400

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    new_scan = Scan(
        patient_name=patient_name,
        notes=notes,
        image_filename=filename,
        analyzed=False
    )
    db.session.add(new_scan)
    db.session.commit()

    return jsonify({'message': f'Scan saved for {patient_name}', 'image_url': f'/static/uploads/scans/{filename}'})

@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.get_json()
        input_list = data.get('input')
        if not input_list or not isinstance(input_list, list):
            return jsonify({'error': 'Input must be a list of numbers.'}), 400
        result = predict(input_list)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------
#  INITIALIZE DATABASE & RUN APP
# ---------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
