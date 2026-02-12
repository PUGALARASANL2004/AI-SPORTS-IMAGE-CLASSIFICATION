# 🏆 Sports Image Classification - AI-Powered Django Application

A professional Django web application that uses deep learning to classify sports images across 100 different sports categories. Built with TensorFlow/Keras and EfficientNet architecture.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.15-orange.svg)

## 🌟 Features

- **AI-Powered Classification**: Uses pre-trained EfficientNet model for accurate sport detection
- **Modern UI/UX**: Dark-themed, responsive interface with glassmorphism effects
- **Drag & Drop Upload**: Intuitive file upload with preview
- **Real-time Prediction**: Instant classification with confidence scores
- **100 Sports Categories**: Comprehensive coverage of various sports activities
- **Admin Interface**: Django admin for managing uploads and viewing predictions

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB+ RAM (for TensorFlow)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. **IMPORTANT: Add Your Trained Model**

Since you have a trained model from Kaggle, follow these steps:

#### Option A: Using .h5 Keras Model
1. Place your trained model file in the `models/` folder
2. Rename it to: `sports_classifier.h5`

```bash
models/
└── sports_classifier.h5    # Your trained model goes here
```

#### Option B: Using PyTorch Model
If your model is in PyTorch format (.pt or .pth), you'll need to modify `ai_model/model_loader.py` to load PyTorch models instead. Let me know if you need help with this.

### 3. Add Class Labels

Create a text file with all 100 sports categories (one per line):

```bash
models/
├── sports_classifier.h5
└── class_labels.txt    # List of 100 sports names, one per line
```

Example `class_labels.txt`:
```
air hockey
ampute football
archery
arm wrestling
...
(100 total sports)
```

> **Note**: The class labels should match the order used during model training. Extract this from your Kaggle dataset.

### 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account for accessing `/admin/`.

### 6. Start the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 📁 Project Structure

```
SPORTS_IMAGE_PREDICTIONS/
├── sports_classifier/          # Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI application
├── classifier/                 # Main Django app
│   ├── models.py              # UploadedImage model
│   ├── views.py               # Upload & result views
│   ├── forms.py               # ImageUploadForm
│   ├── urls.py                # App URL patterns
│   ├── admin.py               # Admin interface
│   ├── templates/             # HTML templates
│   │   └── classifier/
│   │       ├── base.html      # Base template
│   │       ├── upload.html    # Upload page
│   │       └── result.html    # Result page
│   └── static/                # CSS & JavaScript
│       └── classifier/
│           ├── styles.css     # Custom styling
│           └── script.js      # Upload interactions
├── ai_model/                   # AI/ML utilities
│   ├── model_loader.py        # Model loading (singleton)
│   ├── predictor.py           # Prediction logic
│   └── preprocessing.py       # Image preprocessing
├── models/                     # Model files directory
│   ├── sports_classifier.h5   # YOUR TRAINED MODEL
│   └── class_labels.txt       # 100 sports labels
├── media/                      # Uploaded images
│   └── uploads/
├── manage.py                   # Django management
└── requirements.txt            # Python dependencies
```

## 🎯 How It Works

### 1. Image Upload
- User uploads a sports image via drag-and-drop or file browser
- Client-side validation checks format (JPG/PNG) and size (<10MB)
- Image preview shown before submission

### 2. AI Processing
- Image is saved to `media/uploads/`
- Preprocessed to 224×224 pixels with RGB normalization
- Fed through EfficientNet model for classification
- Top prediction and confidence score extracted

### 3. Result Display
- Predicted sport label shown with confidence percentage
- Visual progress bar for confidence score
- Option to upload another image

## 🔧 Configuration

### Model Settings

Edit `ai_model/model_loader.py` if you need to:
- Change model path
- Use different architecture (ResNet, MobileNet)
- Modify preprocessing steps

### Upload Limits

Edit `classifier/forms.py` to change:
- Maximum file size (default: 10MB)
- Allowed formats (default: JPG, PNG)

### Static/Media Files

Production settings in `sports_classifier/settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 📊 Admin Interface

Access at: `http://127.0.0.1:8000/admin/`

Features:
- View all uploaded images
- See prediction results
- Filter by sport category
- Search by image ID

## 🧪 Testing

### Test Image Upload
1. Open `http://127.0.0.1:8000/`
2. Upload a sports image
3. Verify prediction accuracy
4. Check confidence score

### Test with Sample Images
Download test images from the Kaggle dataset validation set to verify model accuracy.

## 🚀 Deployment

### For Production:

1. **Update Settings**:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```

2. **Collect Static Files**:
```bash
python manage.py collectstatic
```

3. **Use Production Server**:
   - Gunicorn, uWSGI, or similar
   - Nginx for serving static/media files

4. **Database**: Consider PostgreSQL or MySQL for production

### Deployment Platforms:
- **Render**: Free tier available
- **Railway**: Easy deployment
- **PythonAnywhere**: Django-friendly
- **AWS/GCP/Azure**: Full control

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirects to upload page |
| `/upload/` | GET/POST | Image upload form |
| `/result/<uuid>/` | GET | Display prediction result |
| `/admin/` | GET | Django admin interface |
| `/media/uploads/...` | GET | Serve uploaded images |

## 🛠️ Troubleshooting

### Model Not Loading
**Error**: `FileNotFoundError: models/sports_classifier.h5`
- **Solution**: Make sure your trained model is in the `models/` folder with the exact name `sports_classifier.h5`

### Class Labels Missing
**Error**: `class_labels.txt not found`
- **Solution**: Create `models/class_labels.txt` with 100 sports names (one per line, matching your training data)

### TensorFlow Warnings
- TensorFlow may show oneDNN warnings - these are safe to ignore
- To suppress: `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'` in settings.py

### Image Upload Fails
- Check file size < 10MB
- Verify format is JPG or PNG
- Ensure `media/` folder has write permissions

## 📚 Technologies Used

- **Backend**: Django 4.2
- **AI/ML**: TensorFlow 2.15, Keras, EfficientNetB0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (development), PostgreSQL (production)
- **Image Processing**: Pillow, NumPy

## 🎓 Dataset Information

**Dataset**: [100 Sports Image Classification](https://www.kaggle.com/datasets/gpiosenka/sports-classification)
- 13,493 training images
- 500 validation images
- 500 test images
- Image size: 224×224 pixels (JPG)
- 100 different sports categories

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django logs: `python manage.py runserver`
3. Verify model and labels are correctly placed

## 📄 License

This project was created for educational and demonstration purposes.

---

**Built with ❤️ using Django + TensorFlow**
