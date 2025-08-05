# 🍅 TomatoHealth - AI-Powered Tomato Disease Detection

TomatoHealth is a comprehensive web application that uses artificial intelligence to detect and diagnose diseases in tomato plants. Built with Flask and TensorFlow, it provides farmers and gardeners with instant, accurate disease identification and treatment recommendations.

## 🌟 Features

### 🔐 User Authentication
- **Secure Registration & Login**: Bcrypt password hashing with session management
- **User Dashboard**: Personalized experience with statistics and history
- **Profile Management**: Secure user data handling

### 🔬 AI-Powered Disease Detection
- **10 Disease Classifications**: Detects major tomato diseases including:
  - Bacterial Spot
  - Early Blight
  - Late Blight
  - Leaf Mold
  - Septoria Leaf Spot
  - Spider Mites (Two-spotted spider mite)
  - Target Spot
  - Yellow Leaf Curl Virus
  - Mosaic Virus
  - Healthy Plants

### 📱 Responsive Design
- **Mobile-First**: Perfect on phones, tablets, and desktops
- **Modern UI**: Bootstrap 5 with custom agricultural theme
- **Touch-Friendly**: Optimized for all interaction methods

### 🖼️ Image Upload & Processing
- **Drag & Drop**: Intuitive file upload interface
- **Real-time Preview**: See images before analysis
- **File Validation**: Automatic type and size checking
- **Multiple Formats**: Support for JPG, JPEG, PNG

### 📊 Comprehensive Analytics
- **Confidence Scores**: Detailed prediction certainty
- **Treatment Recommendations**: Actionable advice for each disease
- **History Tracking**: Complete record of all diagnoses
- **Statistics Dashboard**: Visual insights into plant health

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tomato-disease-detection.git
cd tomato-disease-detection
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your settings (optional for local development)
nano .env
```

### 5. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6. Copy Model File
Make sure the TensorFlow Lite model is in place:
```bash
# The model should be at: Plant_Disease_Prediction/tomato_disease_model.tflite
# Verify the file exists:
ls -la Plant_Disease_Prediction/tomato_disease_model.tflite
```

### 7. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
tomato-disease-detection/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Procfile                       # Heroku deployment configuration
├── runtime.txt                    # Python version specification
├── .env.example                   # Environment variables template
│
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css             # Custom CSS with agricultural theme
│   ├── js/
│   │   └── main.js               # Interactive JavaScript features
│   └── uploads/                  # User uploaded images (created automatically)
│
├── templates/                     # Jinja2 HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── login.html                # User login page
│   ├── register.html             # User registration page
│   ├── dashboard.html            # Main user dashboard
│   ├── predict.html              # Disease prediction interface
│   └── history.html              # Prediction history
│
└── Plant_Disease_Prediction/       # ML model directory
    └── tomato_disease_model.tflite # TensorFlow Lite model file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Required for production
SECRET_KEY=your-super-secret-key-here

# Database (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite:///tomato_disease.db

# File upload settings
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=5242880  # 5MB

# Flask settings
FLASK_ENV=development  # Change to 'production' for deployment
FLASK_DEBUG=True       # Set to False for production
```

### Application Settings

Key configuration options in `app.py`:

- **MAX_CONTENT_LENGTH**: Maximum file upload size (5MB)
- **UPLOAD_FOLDER**: Directory for storing uploaded images
- **Allowed file types**: JPG, JPEG, PNG
- **Model path**: Location of TensorFlow Lite model

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_DEBUG=False
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Initialize Database**
   ```bash
   heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### Alternative Deployment Options

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Manual Server Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY=your-secret-key
export FLASK_ENV=production

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## 📖 Usage Guide

### For End Users

1. **Registration**
   - Visit the application URL
   - Click "Sign up here" on the login page
   - Fill in username, email, and password
   - Agree to terms and create account

2. **Taking Photos**
   - Use good lighting conditions
   - Focus on affected leaves
   - Ensure symptoms are clearly visible
   - Avoid blurry or dark images

3. **Uploading Images**
   - Go to "Diagnose" page
   - Drag and drop image or click to browse
   - Preview image before submission
   - Click "Analyze Image"

4. **Understanding Results**
   - **Disease Name**: Primary diagnosis
   - **Confidence Score**: Model certainty (higher is better)
   - **Treatment Recommendation**: Actionable advice
   - **Top 3 Predictions**: Alternative possibilities

5. **Viewing History**
   - Access all past diagnoses
   - Review treatment recommendations
   - Track plant health over time
   - Export data if needed

### For Developers

#### Adding New Disease Classes
1. Update `DISEASE_CLASSES` list in `app.py`
2. Add corresponding treatments to `DISEASE_TREATMENTS`
3. Retrain TensorFlow model with new classes
4. Update model file
5. Test with sample images

#### Customizing UI
- Edit CSS variables in `static/css/style.css`
- Modify templates in `templates/` directory
- Update JavaScript features in `static/js/main.js`

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    image_filename VARCHAR(120) NOT NULL,
    prediction VARCHAR(120) NOT NULL,
    confidence FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt
- **Session Management**: Secure Flask-Login
- **File Upload Security**: Type and size validation
- **SQL Injection Prevention**: SQLAlchemy ORM
- **XSS Protection**: Jinja2 auto-escaping
- **CSRF Protection**: Flask-WTF integration

## 🎨 Design Features

- **Agricultural Theme**: Green color palette with nature-inspired design
- **Responsive Layout**: Mobile-first Bootstrap 5 implementation
- **Interactive Elements**: Smooth animations and hover effects
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support
- **Loading States**: Visual feedback during processing
- **Error Handling**: User-friendly error messages

## 🧪 Testing

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Image upload and validation
- [ ] Disease prediction accuracy
- [ ] Mobile responsiveness
- [ ] Error handling
- [ ] Navigation and UX flow

### Automated Testing (Future Enhancement)
```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# UI tests
python -m pytest tests/ui/
```

## 🔄 Model Information

The TensorFlow Lite model (`tomato_disease_model.tflite`) is trained on the PlantVillage dataset and can classify 10 different conditions:

- **Input**: 256x256 RGB images
- **Output**: 10-class probability distribution
- **Accuracy**: ~95% on test dataset
- **Model Size**: ~8.5MB (optimized for web deployment)

### Model Requirements
- TensorFlow Lite Runtime
- Image preprocessing: Resize to 256x256, normalize
- Output interpretation: Argmax for class, softmax for confidence

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**
   ```
   Error: Model file not found
   Solution: Ensure tomato_disease_model.tflite is in Plant_Disease_Prediction/
   ```

2. **Database Connection Error**
   ```
   Error: Unable to connect to database
   Solution: Check DATABASE_URL in .env file
   ```

3. **File Upload Issues**
   ```
   Error: File too large
   Solution: Check MAX_CONTENT_LENGTH setting
   ```

4. **Module Import Errors**
   ```
   Error: ModuleNotFoundError
   Solution: Verify virtual environment is activated and requirements installed
   ```

### Performance Optimization

- **Image Compression**: Automatically resize large images
- **Caching**: Implement Redis for session storage
- **CDN**: Use CloudFront for static assets
- **Database**: Optimize queries with indexing

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use semantic HTML5
- Write responsive CSS
- Add comments for complex logic
- Test on multiple devices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PlantVillage Dataset**: For providing the training data
- **TensorFlow Team**: For the machine learning framework
- **Flask Community**: For the excellent web framework
- **Bootstrap Team**: For the responsive CSS framework

## 📞 Support

- **Documentation**: Check this README and inline comments
- **Issues**: Report bugs via GitHub Issues
- **Email**: your-email@example.com
- **Discord**: Join our community server

## 🔮 Future Enhancements

- [ ] Real-time disease detection via camera
- [ ] Multi-language support
- [ ] Weather integration for prevention tips
- [ ] Community features and plant sharing
- [ ] Mobile app development
- [ ] Advanced analytics and reporting
- [ ] Integration with agricultural databases
- [ ] Batch processing for multiple images

---

**Made with ❤️ for farmers and gardeners worldwide**

*Protecting crops with the power of AI*
