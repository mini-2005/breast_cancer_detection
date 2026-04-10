# 🧬 Cancer Detection and Prediction System

## 📌 Overview
This project is a web-based application that detects and predicts cancer using deep learning and machine learning techniques. It helps in early diagnosis by analyzing medical images and patient data.

The system uses:
- CNN + LSTM for cancer detection from images  
- Random Forest for prediction based on extracted features  

It helps identify whether cancer is:
- Benign (Non-cancerous)
- Malignant (Cancerous)

---

## 🚀 Features
- 🔐 User Authentication (Login & Signup)
- 🏠 Home page with project overview
- 📤 Upload medical images for detection
- 🔍 Cancer detection using CNN + LSTM model
- 📊 Cancer prediction using Random Forest
- 👤 Patient details form and record handling
- 🛠️ Admin dashboard for monitoring
- 🎨 Clean and responsive UI

---

## 🛠️ Tech Stack
- Python
- Django
- TensorFlow / Keras
- Scikit-learn
- OpenCV
- HTML, CSS

---

## 📂 Project Structure
cancer_detection/              # Root folder  
cancer_detection/              # Django project  
predictor/                     # App  
templates/                     # HTML files  
media/                         # Uploaded images  
breast_cancer_model.pkl        # Random Forest model  
cancer_detection_model.h5                   # CNN + LSTM model  
manage.py  

---

## ▶️ How to Run

1. Clone the repository  
git clone https://github.com/your-username/cancer-detection-project.git  

2. Navigate to project folder  
cd cancer-detection-project  

3. Install dependencies  
pip install -r requirements.txt  

4. Run server  
python manage.py runserver  

---

## 📸 Screenshots
### 🔐 Login / Signup
![Home](screenshots/login.png)

### 🏠 Home Page
![Home](screenshots/home.png)

### 🔍 Detection Page
![Home](screenshots/detection.png)

### ✅ Result Output
![Home](screenshots/result.png)

### 📊 Prediction Output
![Home](screenshots/prediction.png)

---

## ⚙️ Use Case
This project can be used in the healthcare domain to assist doctors in early cancer detection and prediction, reducing manual effort and improving diagnostic accuracy.

---

## 🎯 Future Improvements
- Real-time detection using medical imaging devices
- Cloud deployment (AWS / Render)
- Improve model accuracy with larger datasets
- Add multi-cancer detection support

---

## 👨‍💻 Author
MANICKARASI N A