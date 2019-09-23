from django.urls import path, include
from . import views

app_name = 'tools'
urlpatterns = [
    path('<str:data>/', views.generate_qrcode, name='index'),
]
