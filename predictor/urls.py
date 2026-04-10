from django.contrib import admin
from django.urls import path
from predictor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('detection/', views.detection, name='detection'),
    path('patients/',views.patients,name='patients'),
    path('', views.login_view, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('admin-login/',views.admin_login,name="admin_login"),
    path('admin-dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('download-patients/', views.download_patients, name='download_patients'),
    path('clinical/', views.clinical_prediction, name='clinical_prediction'),
    
]
