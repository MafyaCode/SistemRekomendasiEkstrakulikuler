# import library yang dibutuhkan
import pandas as pd
import numpy as np
import os

# --- Konfigurasi ---
JUMLAH_SISWA = 200  # Tentukan berapa banyak data siswa fiktif yang ingin dibuat
KATEGORI_MINAT = [
    'Olahraga_Tim_Kompetisi',
    'Olahraga_Individu_Kebugaran',
    'Seni_Bela_Diri_Disiplin',
    'Musik_Seni_Pertunjukan',
    'Aktivitas_Outdoor_Petualangan',
    'Seni_Visual_Kreativitas',
    'Teknologi_Media',
    'Kepemimpinan_Organisasi',
    'Sosial_Komunikasi',
    'Nasionalisme_Baris'
] # Sesuaikan dengan daftar minat final Anda
NAMA_FILE_OUTPUT = 'data_siswa_minat_sintetis.csv'
# Tentukan path folder 'data' relatif terhadap lokasi script ini
# Jika script ini dijalankan dari folder 'backend', path ke folder 'data' adalah '../data'
# Jika script ini dijalankan dari root proyek, pathnya adalah 'data'
LOKASI_FOLDER_DATA = '../data' # Asumsi script dijalankan dari folder 'backend'
# Atau LOKASI_FOLDER_DATA = 'data' # Jika script dijalankan dari root proyek

# --- Pembuatan Data ---

# 1. Buat ID Siswa (contoh: S001, S002, ...)
id_siswa = [f'S{str(i+1).zfill(3)}' for i in range(JUMLAH_SISWA)]

# 2. Buat Skor Minat Acak (nilai 1 s/d 5)
# np.random.randint(1, 6, size=(JUMLAH_SISWA, len(KATEGORI_MINAT)))
# menghasilkan matriks berukuran JUMLAH_SISWA baris x jumlah KATEGORI_MINAT kolom
# dengan nilai integer acak antara 1 (inklusif) dan 6 (eksklusif) -> yaitu 1, 2, 3, 4, 5
skor_minat = np.random.randint(1, 6, size=(JUMLAH_SISWA, len(KATEGORI_MINAT)))

# 3. Gabungkan ID Siswa dan Skor Minat menjadi DataFrame Pandas
# Buat dictionary untuk data
data = {'id_siswa': id_siswa}
# Tambahkan skor minat ke dictionary dengan nama kolom sesuai kategori minat
for i, nama_minat in enumerate(KATEGORI_MINAT):
    # Menggunakan nama kategori sebagai kunci kolom, dan mengambil kolom skor ke-i
    data[f'minat_{nama_minat.lower()}'] = skor_minat[:, i]

# Buat DataFrame
df_siswa_minat = pd.DataFrame(data)

# --- Penyimpanan ke CSV ---

# Pastikan folder 'data' ada, jika tidak, buat folder tersebut
if not os.path.exists(LOKASI_FOLDER_DATA):
    os.makedirs(LOKASI_FOLDER_DATA)
    print(f"Folder '{LOKASI_FOLDER_DATA}' telah dibuat.")

# Tentukan path lengkap untuk file output
path_output = os.path.join(LOKASI_FOLDER_DATA, NAMA_FILE_OUTPUT)

# Simpan DataFrame ke file CSV
# index=False agar nomor index DataFrame tidak ikut ditulis ke file CSV
df_siswa_minat.to_csv(path_output, index=False)

print(f"File '{NAMA_FILE_OUTPUT}' berhasil dibuat di folder '{LOKASI_FOLDER_DATA}' dengan {JUMLAH_SISWA} data siswa.")
print("\nContoh 5 baris pertama data:")
print(df_siswa_minat.head().to_markdown(index=False)) # Menampilkan 5 baris pertama dalam format markdown
 