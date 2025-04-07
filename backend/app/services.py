# backend/app/services.py

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import joblib # Untuk menyimpan dan memuat model/scaler
import os
import matplotlib.pyplot as plt # Untuk Elbow Method

# --- Konfigurasi Path ---
# Asumsi script/fungsi ini dijalankan dari dalam folder 'backend'
# Path relatif ke folder data
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
# Path relatif ke folder untuk menyimpan model terlatih
MODEL_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'models') # Buat folder 'models' di dalam 'backend'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, 'data_siswa_minat_sintetis.csv')
MODEL_FILE_PATH = os.path.join(MODEL_FOLDER, 'kmeans_model.joblib')
SCALER_FILE_PATH = os.path.join(MODEL_FOLDER, 'scaler.joblib')
ELBOW_PLOT_PATH = os.path.join(MODEL_FOLDER, 'elbow_method.png') # Path untuk menyimpan plot elbow

# --- Fungsi Pelatihan Model K-Means ---

def train_kmeans_model(csv_path=CSV_FILE_PATH, n_clusters=5, model_save_path=MODEL_FILE_PATH, scaler_save_path=SCALER_FILE_PATH):
    """
    Melatih model K-Means berdasarkan data minat siswa dari file CSV.

    Args:
        csv_path (str): Path ke file CSV data minat siswa.
        n_clusters (int): Jumlah cluster (k) yang diinginkan. Perlu ditentukan secara optimal.
        model_save_path (str): Path untuk menyimpan model K-Means terlatih.
        scaler_save_path (str): Path untuk menyimpan objek MinMaxScaler.

    Returns:
        tuple: Berisi (model K-Means terlatih, scaler) jika berhasil, atau (None, None) jika gagal.
    """
    print(f"Memulai pelatihan model K-Means dengan k={n_clusters}...")
    try:
        # 1. Muat Data
        df = pd.read_csv(csv_path)
        print(f"Data berhasil dimuat dari {csv_path}")

        # 2. Pilih Fitur untuk Clustering (semua kolom kecuali 'id_siswa')
        # Asumsi semua kolom selain 'id_siswa' adalah skor minat
        features = df.drop('id_siswa', axis=1)
        if features.isnull().values.any():
            print("Peringatan: Terdapat nilai null dalam data fitur. Mengisi dengan 0.")
            features = features.fillna(0) # Atau gunakan metode imputasi lain yang lebih canggih

        print(f"Fitur yang digunakan untuk clustering: {list(features.columns)}")

        # 3. Scaling Data (Normalisasi 0-1) - Penting untuk K-Means
        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(features)
        print("Data fitur berhasil di-scaling (MinMaxScaler).")

        # 4. Inisialisasi dan Latih Model K-Means
        kmeans = KMeans(n_clusters=n_clusters,
                        init='k-means++',     # Metode inisialisasi centroid
                        n_init=10,            # Jalankan 10x dengan seed berbeda, pilih yg terbaik
                        max_iter=300,         # Maksimum iterasi per run
                        random_state=42)      # Seed untuk reproduktifitas
        kmeans.fit(scaled_features)
        print(f"Model K-Means berhasil dilatih dengan {n_clusters} clusters.")
        print(f"Inertia (Sum of Squared Errors): {kmeans.inertia_}")
        # Label cluster untuk setiap siswa dalam data training
        # labels = kmeans.labels_
        # print(f"Contoh label cluster untuk 5 data pertama: {labels[:5]}")

        # 5. Simpan Model dan Scaler
        # Pastikan folder model ada
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        os.makedirs(os.path.dirname(scaler_save_path), exist_ok=True)

        joblib.dump(kmeans, model_save_path)
        joblib.dump(scaler, scaler_save_path)
        print(f"Model K-Means disimpan di: {model_save_path}")
        print(f"Scaler disimpan di: {scaler_save_path}")

        return kmeans, scaler

    except FileNotFoundError:
        print(f"Error: File data tidak ditemukan di {csv_path}")
        return None, None
    except Exception as e:
        print(f"Error selama pelatihan K-Means: {e}")
        return None, None

# --- Fungsi untuk Menentukan K Optimal (Elbow Method) ---

def find_optimal_k(csv_path=CSV_FILE_PATH, max_k=15, plot_save_path=ELBOW_PLOT_PATH):
    """
    Mencari jumlah cluster (k) optimal menggunakan Elbow Method dan menyimpan plotnya.

    Args:
        csv_path (str): Path ke file CSV data minat siswa.
        max_k (int): Jumlah cluster maksimum yang akan diuji.
        plot_save_path (str): Path untuk menyimpan gambar plot Elbow Method.
    """
    print("Mencari nilai K optimal menggunakan Elbow Method...")
    try:
        df = pd.read_csv(csv_path)
        features = df.drop('id_siswa', axis=1)
        if features.isnull().values.any():
            features = features.fillna(0)

        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(features)

        inertia = [] # Sum of squared distances of samples to their closest cluster center (WCSS)
        K = range(1, max_k + 1)
        for k in K:
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, random_state=42)
            kmeans.fit(scaled_features)
            inertia.append(kmeans.inertia_)
            print(f"  Menguji k={k}, Inertia={kmeans.inertia_}")

        # Plotting the Elbow Method graph
        plt.figure(figsize=(10, 6))
        plt.plot(K, inertia, 'bo-') # 'bo-' = blue circle marker with solid line
        plt.xlabel('Jumlah Cluster (k)')
        plt.ylabel('Inertia (WCSS)')
        plt.title('Elbow Method untuk Menentukan K Optimal')
        plt.xticks(K)
        plt.grid(True)

        # Simpan plot
        os.makedirs(os.path.dirname(plot_save_path), exist_ok=True)
        plt.savefig(plot_save_path)
        print(f"Plot Elbow Method disimpan di: {plot_save_path}")
        # plt.show() # Tampilkan plot jika dijalankan secara interaktif

        print("Analisis Elbow Method selesai. Periksa plot untuk menemukan 'siku' (elbow point).")

    except FileNotFoundError:
        print(f"Error: File data tidak ditemukan di {csv_path}")
    except Exception as e:
        print(f"Error selama mencari K optimal: {e}")


# --- Fungsi Prediksi Cluster ---

def predict_student_cluster(student_interests, model_path=MODEL_FILE_PATH, scaler_path=SCALER_FILE_PATH):
    """
    Memprediksi cluster untuk data minat seorang siswa.

    Args:
        student_interests (list atau np.array): List atau array berisi skor minat siswa
                                                (harus sesuai urutan fitur saat training).
        model_path (str): Path ke file model K-Means terlatih (.joblib).
        scaler_path (str): Path ke file scaler (.joblib).

    Returns:
        int: Label cluster yang diprediksi, atau None jika terjadi error.
    """
    try:
        # 1. Muat Model dan Scaler
        kmeans = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        # 2. Ubah input menjadi numpy array dan reshape
        # K-Means mengharapkan input 2D (meskipun hanya 1 sampel)
        interests_array = np.array(student_interests).reshape(1, -1)

        # 3. Scaling data input menggunakan scaler yang sama saat training
        scaled_interests = scaler.transform(interests_array)

        # 4. Prediksi Cluster
        cluster_label = kmeans.predict(scaled_interests)

        # Hasil predict adalah array, ambil elemen pertama
        return int(cluster_label[0])

    except FileNotFoundError:
        print(f"Error: File model '{model_path}' atau scaler '{scaler_path}' tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Error saat memprediksi cluster: {e}")
        return None

# --- Contoh Penggunaan (bisa dijalankan langsung untuk testing) ---
if __name__ == '__main__':
    print("Menjalankan contoh penggunaan services K-Means...")

    # 1. (Opsional tapi direkomendasikan) Cari K optimal dulu
    # find_optimal_k(max_k=10) # Uji k dari 1 sampai 10
    # Setelah melihat plot 'elbow_method.png', tentukan nilai K yang paling baik (misal K=4)
    OPTIMAL_K = 4 # Ganti angka ini berdasarkan hasil analisis plot elbow

    # 2. Latih model dengan K optimal
    trained_model, trained_scaler = train_kmeans_model(n_clusters=OPTIMAL_K)

    # 3. Contoh prediksi untuk siswa baru
    if trained_model and trained_scaler:
        # Buat contoh data minat siswa baru (harus sama jumlah & urutan fiturnya)
        # Misal ada 10 kategori minat:
        siswa_baru_minat = [4, 5, 1, 2, 5, 3, 2, 4, 5, 1]
        print(f"\nMemprediksi cluster untuk minat siswa baru: {siswa_baru_minat}")

        predicted_cluster = predict_student_cluster(siswa_baru_minat)

        if predicted_cluster is not None:
            print(f"Siswa baru diprediksi masuk ke Cluster: {predicted_cluster}")
        else:
            print("Gagal melakukan prediksi.")
    else:
        print("Pelatihan model gagal, tidak dapat melanjutkan ke prediksi.")

