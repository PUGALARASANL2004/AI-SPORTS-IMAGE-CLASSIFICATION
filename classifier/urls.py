from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload'),
    # Result page is now handled directly via POST in upload_image

    path('dashboard/', views.dashboard, name='dashboard'),
    path('health/', views.health_check, name='health'),
]
