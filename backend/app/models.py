# backend/app/models.py
from app import db # Import objek db dari __init__.py
from datetime import datetime

class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), index=True, nullable=False)
    kelas = db.Column(db.String(20))
    timestamp_input = db.Column(db.DateTime, default=datetime.utcnow)
    # Relasi: Satu siswa punya banyak input minat
    minat_siswa = db.relationship('MinatSiswa', backref='siswa', lazy='dynamic')

    def __repr__(self):
        return f'<Siswa {self.nama}>'

class Minat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_minat = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi_minat = db.Column(db.Text)
    # Relasi: Satu minat bisa dimiliki banyak siswa (via MinatSiswa)
    siswa_dengan_minat_ini = db.relationship('MinatSiswa', backref='minat', lazy='dynamic')
    # Relasi: Satu minat bisa relevan untuk banyak ekskul (via EkskulMinat)
    ekskul_relevan = db.relationship('EkskulMinat', backref='minat', lazy='dynamic')

    def __repr__(self):
        return f'<Minat {self.nama_minat}>'

class MinatSiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skor = db.Column(db.Integer, nullable=False) # Skor 1-5
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    minat_id = db.Column(db.Integer, db.ForeignKey('minat.id'), nullable=False)

    def __repr__(self):
        return f'<MinatSiswa SiswaID:{self.siswa_id} MinatID:{self.minat_id} Skor:{self.skor}>'

class Ekskul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_ekskul = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi_ekskul = db.Column(db.Text)
    # Relasi: Satu ekskul bisa relevan dengan banyak minat (via EkskulMinat)
    minat_terkait = db.relationship('EkskulMinat', backref='ekskul', lazy='dynamic')

    def __repr__(self):
        return f'<Ekskul {self.nama_ekskul}>'

class EkskulMinat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ekskul_id = db.Column(db.Integer, db.ForeignKey('ekskul.id'), nullable=False)
    minat_id = db.Column(db.Integer, db.ForeignKey('minat.id'), nullable=False)

    def __repr__(self):
        return f'<EkskulMinat EkskulID:{self.ekskul_id} MinatID:{self.minat_id}>'
