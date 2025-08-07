import os
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import cv2

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tomato_disease.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Disease classes
DISEASE_CLASSES = [
    'Bacterial spot',
    'Early blight', 
    'Late blight',
    'Leaf Mold',
    'Septoria leaf spot',
    'Spider mites Two-spotted spider mite',
    'Target Spot',
    'Yellow Leaf Curl Virus',
    'Mosaic virus',
    'Healthy'
]

# Disease treatment recommendations
DISEASE_TREATMENTS = {
    'Bacterial spot': 'Remove affected leaves and apply copper-based fungicides. Improve air circulation.',
    'Early blight': 'Remove infected plant debris. Apply fungicides containing chlorothalonil or copper.',
    'Late blight': 'Remove affected plants immediately. Apply fungicides and ensure good air circulation.',
    'Leaf Mold': 'Reduce humidity and improve ventilation. Apply fungicides if necessary.',
    'Septoria leaf spot': 'Remove lower leaves and apply fungicides. Avoid overhead watering.',
    'Spider mites Two-spotted spider mite': 'Increase humidity around plants. Use miticides or beneficial insects.',
    'Target Spot': 'Remove affected leaves and apply fungicides. Avoid overhead irrigation.',
    'Yellow Leaf Curl Virus': 'Remove infected plants. Control whitefly vectors with insecticides.',
    'Mosaic virus': 'Remove infected plants. Control aphid vectors and use virus-free seeds.',
    'Healthy': 'Your tomato plant looks healthy! Continue with proper care and monitoring.'
}

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Prediction model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(120), nullable=False)
    prediction = db.Column(db.String(120), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_plant_image(image_path):
    """
    Basic plant detection using color analysis and edge detection.
    This is a simple heuristic - for production, you'd want a dedicated plant detection model.
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Define green color range (plants are typically green)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Create mask for green regions
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Calculate percentage of green pixels
        total_pixels = image.shape[0] * image.shape[1]
        green_pixels = cv2.countNonZero(green_mask)
        green_percentage = (green_pixels / total_pixels) * 100
        
        # Edge detection to find leaf-like structures
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate edge density
        edge_pixels = cv2.countNonZero(edges)
        edge_percentage = (edge_pixels / total_pixels) * 100
        
        # Simple heuristic: if there's significant green color and some edges, it might be a plant
        is_likely_plant = green_percentage > 15 and edge_percentage > 2
        
        # Additional check: look for organic shapes (leaves typically have rounded edges)
        # This is a simplified check - in reality you'd want more sophisticated shape analysis
        
        return is_likely_plant
        
    except Exception as e:
        print(f"Error in plant detection: {e}")
        return False

def validate_image_content(image_path):
    """
    Validate that the image contains plant material suitable for disease analysis.
    Returns (is_valid, message)
    """
    try:
        # Check if image is a plant
        if not is_plant_image(image_path):
            return False, "The uploaded image doesn't appear to contain plant material. Please upload a clear photo of a tomato leaf or plant."
        
        # Additional checks can be added here
        # - Check image quality (blur, lighting)
        # - Check if the plant part is clearly visible
        # - Check minimum size requirements
        
        return True, "Image validation passed."
        
    except Exception as e:
        return False, f"Error validating image: {str(e)}"

# Load TensorFlow Lite model
class TomatoDiseasePredictor:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
    
    def predict(self, image):
        # Preprocess image
        if isinstance(image, str):
            image = Image.open(image)
        elif hasattr(image, 'read'):
            image = Image.open(image)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size
        image = image.resize((256, 256))
        
        # Convert to array and normalize
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # Add batch dimension
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], input_arr)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get predictions
        predictions = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Get prediction class and confidence
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        return predicted_class, confidence, predictions[0]

# Initialize the model
try:
    model_path = os.path.join('Plant_Disease_Prediction', 'tomato_disease_model.tflite')
    if os.path.exists(model_path):
        predictor = TomatoDiseasePredictor(model_path)
    else:
        predictor = None
        print("Warning: Model file not found. Please ensure tomato_disease_model.tflite is in the Plant_Disease_Prediction directory.")
except Exception as e:
    predictor = None
    print(f"Warning: Could not load model: {e}")

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
                                        .order_by(Prediction.timestamp.desc())\
                                        .limit(5).all()
    
    return render_template('dashboard.html', 
                         total_predictions=total_predictions,
                         recent_predictions=recent_predictions)

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload JPG, JPEG, or PNG files.', 'error')
            return redirect(request.url)
        
        if not predictor:
            flash('Model not available. Please contact administrator.', 'error')
            return redirect(request.url)
        
        try:
            # Save uploaded file
            filename = save_uploaded_file(file)
            if not filename:
                flash('Error saving file', 'error')
                return redirect(request.url)
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Validate image content before classification
            is_valid, validation_message = validate_image_content(file_path)
            if not is_valid:
                # Delete the uploaded file since it's not valid
                try:
                    os.remove(file_path)
                except:
                    pass
                flash(validation_message, 'error')
                return redirect(request.url)
            
            # Make prediction
            predicted_class, confidence, all_predictions = predictor.predict(file_path)
            
            # Additional confidence threshold check
            if confidence < 0.3:  # Less than 30% confidence
                flash('The image quality is too low for reliable disease detection. Please upload a clearer image of a tomato leaf.', 'error')
                try:
                    os.remove(file_path)
                except:
                    pass
                return redirect(request.url)
            
            disease_name = DISEASE_CLASSES[predicted_class]
            treatment = DISEASE_TREATMENTS[disease_name]
            
            # Get top 3 predictions
            top_3_indices = np.argsort(all_predictions)[-3:][::-1]
            top_3_predictions = [(DISEASE_CLASSES[i], float(all_predictions[i]) * 100) 
                               for i in top_3_indices]
            
            # Save prediction to database
            prediction_record = Prediction(
                user_id=current_user.id,
                image_filename=filename,
                prediction=disease_name,
                confidence=confidence * 100
            )
            db.session.add(prediction_record)
            db.session.commit()
            
            return render_template('predict.html', 
                                 prediction=True,
                                 disease_name=disease_name,
                                 confidence=confidence * 100,
                                 treatment=treatment,
                                 image_filename=filename,
                                 top_predictions=top_3_predictions)
        
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('predict.html', prediction=False)

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
                                 .order_by(Prediction.timestamp.desc())\
                                 .paginate(page=page, per_page=10, error_out=False)
    return render_template('history.html', predictions=predictions)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))