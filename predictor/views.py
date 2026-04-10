import numpy as np
import cv2
import tensorflow as tf
import csv

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from sklearn.preprocessing import LabelEncoder
import pickle

from .models import Patient


# Load trained AI model
model = tf.keras.models.load_model("cancer_detection_model.h5")


# Home Page
def home(request):
    return render(request, "home.html")



# ---------------------------
# USER SIGNUP
# ---------------------------
def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "signup.html")


# ---------------------------
# USER LOGIN
# ---------------------------
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            return render(request, "login.html", {
                "error": "Invalid login credentials"
            })

    return render(request, "login.html")


# ---------------------------
# USER LOGOUT
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------
# CANCER DETECTION PAGE
# ---------------------------
@login_required
def detection(request):

    prediction = None
    image_url = None
    result_type = None

    if request.method == "POST":

        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        symptoms = request.POST.get("symptoms")

        image = request.FILES.get("image")

        # Save patient first
        patient = Patient.objects.create(
            user=request.user,
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            email=email,
            symptoms=symptoms,
            image=image
        )

        image_url = patient.image.url

        # Image preprocessing
        img_path = patient.image.path
        img = cv2.imread(img_path)
        img = cv2.resize(img, (64, 64))
        img = img / 255.0
        img = np.reshape(img, (1, 64, 64, 3))

        # Prediction
        pred = model.predict(img)
        predicted_class = np.argmax(pred)

        if predicted_class == 1:
            prediction = "Malignant Tumor Detected"
            result_type = "danger"
        else:
            prediction = "Benign Tumor Detected"
            result_type = "good"

        # Save result
        patient.result = prediction
        patient.save()

    return render(request, "detection.html", {
        "prediction": prediction,
        "image_url": image_url,
        "result_type": result_type
    })


# ---------------------------
# PATIENT RECORDS
# ---------------------------
@login_required
def patients(request):

    if request.user.is_superuser:
        patient_list = Patient.objects.all().order_by('-date')
    else:
        patient_list = Patient.objects.filter(user=request.user).order_by('-date')

    return render(request, "patients.html", {
        "patients": patient_list
    })


# ---------------------------
# ADMIN LOGIN
# ---------------------------
def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            else:
                return render(request, "admin_login.html", {
                    "error": "You are not an admin"
                })

        else:
            return render(request, "admin_login.html", {
                "error": "Invalid Admin Credentials"
            })

    return render(request, "admin_login.html")


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect("home")

    total_patients = Patient.objects.count()

    cancer_cases = Patient.objects.filter(
        result__icontains="Malignant"
    ).count()

    normal_cases = Patient.objects.filter(
        result__icontains="Benign"
    ).count()

    patients = Patient.objects.all().order_by('-date')[:10]

    context = {
        "total": total_patients,
        "cancer": cancer_cases,
        "normal": normal_cases,
        "patients": patients
    }

    return render(request, "admin_dashboard.html", context)
@login_required
def download_patients(request):

    if not request.user.is_superuser:
        return redirect("home")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_records.csv"'

    writer = csv.writer(response)

    # Table header
    writer.writerow([
        "Name",
        "Age",
        "Gender",
        "Phone",
        "Email",
        "Symptoms",
        "Result",
        "Date"
    ])

    patients = Patient.objects.all()

    for p in patients:
        writer.writerow([
            p.name,
            p.age,
            p.gender,
            p.phone,
            p.email,
            p.symptoms,
            p.result,
            p.date
        ])

    return response

model_ml = pickle.load(open("breast_cancer_model.pkl", "rb"))
@login_required
def clinical_prediction(request):

    result = None
    result_type = None

    if request.method == "POST":

        age = int(request.POST.get("age"))
        lump = request.POST.get("lump")
        family = request.POST.get("family_history")
        prev = request.POST.get("previous_issue")
        hormonal = request.POST.get("hormonal")
        breast = request.POST.get("breastfeeding")
        nipple = request.POST.get("nipple_change")

        # Encode inputs (same as training)
        le = LabelEncoder()

        data = [
            age,
            le.fit_transform([lump])[0],
            le.fit_transform([family])[0],
            le.fit_transform([prev])[0],
            le.fit_transform([hormonal])[0],
            le.fit_transform([breast])[0],
            le.fit_transform([nipple])[0],
        ]

        prediction = model_ml.predict([data])[0]

        if prediction == "High":
            result = "⚠️ High Risk of Breast Cancer"
            result_type = "high"
        elif prediction == "Medium":
            result = "⚠️ Medium Risk"
            result_type = "medium"
        else:
            result = "✅ Low Risk"
            result_type = "low"

    return render(request, "clinical_prediction.html", {
        "result": result,
        "result_type": result_type
    })