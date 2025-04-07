# backend/run.py
from app import create_app, db # Import create_app dan db
from app.models import Siswa, Minat, MinatSiswa, Ekskul, EkskulMinat # Import semua model

# Buat instance aplikasi
app = create_app()

# Membuat shell context agar bisa akses db dan model via 'flask shell'
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Siswa': Siswa, 'Minat': Minat, 'MinatSiswa': MinatSiswa,
            'Ekskul': Ekskul, 'EkskulMinat': EkskulMinat}

if __name__ == '__main__':
     # Jalankan aplikasi (hanya untuk development)
     # Host='0.0.0.0' agar bisa diakses dari luar container/VM jika perlu
     # Debug=True agar otomatis restart saat ada perubahan kode & tampilkan error detail    
     app.run(host='0.0.0.0', port=5000, debug=True)
