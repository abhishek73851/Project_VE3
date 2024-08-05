# analyzer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_csv, name="upload_csv"),
    path("app/<int:user_id>/", views.analyze_csv, name="analyze_csv"),
]
