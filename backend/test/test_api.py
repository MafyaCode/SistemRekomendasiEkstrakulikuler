import requests
import json

# URL endpoint API
url = "http://127.0.0.1:5000/api/rekomendasi"

# Data minat siswa yang ingin diuji (sesuaikan!)
# Pastikan jumlahnya sesuai dengan jumlah fitur minat (misal, 10)
data_minat = {"interests": [1, 2, 5, 4, 2, 5, 3, 1, 2, 5]}

# Header untuk menandakan kita mengirim JSON
headers = {'Content-Type': 'application/json'}

print(f"Mengirim data ke {url}: {data_minat}")

try:
    # Kirim request POST
    response = requests.post(url, headers=headers, data=json.dumps(data_minat))

    # Cek status code respons
    if response.status_code == 200:
        print("\n--- Respons Sukses ---")
        # Tampilkan hasil JSON
        hasil = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Cluster Prediksi: {hasil.get('cluster')}")
        print(f"Rekomendasi Ekskul: {hasil.get('rekomendasi')}")
    else:
        print(f"\n--- Error ---")
        print(f"Status Code: {response.status_code}")
        try:
            # Coba tampilkan pesan error dari JSON jika ada
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            # Jika respons bukan JSON, tampilkan teks mentah
            print(response.text)

except requests.exceptions.ConnectionError as e:
    print(f"\n--- Error Koneksi ---")
    print(f"Tidak dapat terhubung ke server. Pastikan server Flask berjalan di {url}.")
    print(f"Detail error: {e}")
except Exception as e:
    print(f"\n--- Error Lain ---")
    print(f"Terjadi error: {e}")

