# backend/config.py
import os

# Dapatkan direktori dasar proyek backend
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-yang-sulit-ditebak' # Ganti dengan kunci acak yang kuat
    # Konfigurasi Database SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') # Ini akan membuat file app.db di folder backend
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Nonaktifkan fitur track modifikasi yg tidak perlu

