# backend/app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Inisialisasi ekstensi di level modul (tanpa app)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Membuat instance aplikasi Flask
    app = Flask(__name__)
    # Memuat konfigurasi dari objek Config
    app.config.from_object(config_class)

    # Mengaktifkan CORS
    CORS(app)

    # Mengikat ekstensi database ke instance aplikasi spesifik INI
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Definisi Route untuk Halaman Utama ---
    @app.route('/')
    @app.route('/index')
    def index():
        """Route untuk halaman utama/root."""
        # Anda bisa merender template HTML di sini jika mau
        # return render_template('index.html')
        # Untuk sekarang, kita kembalikan string HTML sederhana:
        return "<h1>Server Backend Aktif</h1><p>Selamat datang di server backend sistem rekomendasi.</p><p>API endpoint ada di /api/</p>"
    # -----------------------------------------

    # --- Impor dan Registrasi Komponen Aplikasi Lain ---
    with app.app_context():
        # Import models agar dikenali oleh Flask-Migrate
        from . import models

        # --- Mendaftarkan Blueprint API ---
        from . import routes # Import modul routes.py
        app.register_blueprint(routes.bp) # Daftarkan blueprint 'bp' dari routes.py
        # -----------------------------

    return app

