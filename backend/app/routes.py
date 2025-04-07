# backend/app/routes.py

from flask import Blueprint, request, jsonify
# Import fungsi prediksi dari services
from .services import predict_student_cluster
# Import db jika perlu query database di route lain nanti
# from . import db

# --- Membuat Blueprint ---
# Semua route terkait API akan masuk ke blueprint ini
bp = Blueprint('api', __name__, url_prefix='/api')

# --- Logika Rekomendasi (PENTING: Perlu Disesuaikan!) ---
# Pastikan mapping ini sudah sesuai dengan analisis cluster Anda
CLUSTER_TO_EKSKUL_MAP = {
    0: ["OSIS", "Paskibra"],
    1: ["Futsal", "Basket", "Bulutangkis"],
    2: ["Fotografi", "Paduan Suara"],
    3: ["Pecinta Alam", "Silat", "Karate"]
    # Sesuaikan berdasarkan OPTIMAL_K dan analisis cluster
}

# --- Definisi API Endpoint pada Blueprint ---

@bp.route('/rekomendasi', methods=['POST'])
def get_rekomendasi():
    """
    Endpoint API untuk menerima data minat siswa dan mengembalikan rekomendasi ekskul.
    Input: JSON {"interests": [skor1, skor2, ..., skorN]}
    Output: JSON {"cluster": cluster_label, "rekomendasi": [ekskul1, ekskul2, ...]}
    """
    data = request.get_json()

    # Validasi Input
    if not data or 'interests' not in data:
        return jsonify({"error": "Input JSON tidak valid. Harus ada key 'interests'."}), 400

    student_interests = data['interests']

    if not isinstance(student_interests, list):
        return jsonify({"error": "'interests' harus berupa list skor."}), 400

    # Sesuaikan angka 10 jika jumlah kategori minat Anda berbeda
    JUMLAH_FITUR_MINAT = 10
    if len(student_interests) != JUMLAH_FITUR_MINAT:
        return jsonify({"error": f"Jumlah skor minat harus {JUMLAH_FITUR_MINAT}."}), 400

    print(f"Menerima request rekomendasi untuk minat: {student_interests}")

    # Prediksi Cluster
    predicted_cluster = predict_student_cluster(student_interests)

    # Dapatkan Rekomendasi
    if predicted_cluster is not None:
        print(f"Hasil prediksi cluster: {predicted_cluster}")
        rekomendasi_ekskul = CLUSTER_TO_EKSKUL_MAP.get(predicted_cluster, [])

        if not rekomendasi_ekskul:
            print(f"Peringatan: Tidak ada pemetaan ekskul ditemukan untuk cluster {predicted_cluster}.")

        # Kirim Respons Sukses
        return jsonify({
            "cluster": predicted_cluster,
            "rekomendasi": rekomendasi_ekskul
        })
    else:
        # Kirim Respons Error jika prediksi gagal
        print("Error saat prediksi cluster.")
        return jsonify({"error": "Gagal memproses prediksi cluster."}), 500

# --- Route Tambahan (Contoh: Halaman Index API) ---
# Kita daftarkan juga di blueprint 'api' agar konsisten
# URL-nya akan menjadi /api/ karena url_prefix blueprint
@bp.route('/', methods=['GET'])
def api_index():
    """Route index untuk blueprint API."""
    return "<h1>API Sistem Rekomendasi Aktif</h1><p>Gunakan endpoint /api/rekomendasi [POST]</p>"

# Anda bisa menambahkan endpoint lain di blueprint 'api' ini jika perlu
# @bp.route('/ekskul', methods=['GET'])
# def get_all_ekskul():
#     # Logika untuk mengambil semua ekskul dari database
#     pass
