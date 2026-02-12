from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload'),
    path('result/<uuid:pk>/', views.result_view, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
