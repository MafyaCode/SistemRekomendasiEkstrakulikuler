// --- Konfigurasi ---
const API_URL = '[http://127.0.0.1:5000/api/rekomendasi](http://127.0.0.1:5000/api/rekomendasi)'; // URL API Backend Flask Anda

// Daftar Kategori Minat (HARUS SAMA DENGAN YANG DIGUNAKAN DI BACKEND/DATA)
const KATEGORI_MINAT = [
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
];
const JUMLAH_MINAT = KATEGORI_MINAT.length;

// --- Referensi Elemen DOM ---
// Dapatkan elemen setelah DOM siap
let inputsContainer, loadingInputs, submitButton, loadingSpinner, resultsArea, clusterResult, recommendationsDiv, errorMessage;

// --- Fungsi Inisialisasi ---
function initializeDOMReferences() {
    inputsContainer = document.getElementById('interest-inputs');
    loadingInputs = document.getElementById('loading-inputs');
    submitButton = document.getElementById('submit-button');
    loadingSpinner = document.getElementById('loading-spinner');
    resultsArea = document.getElementById('results-area');
    clusterResult = document.getElementById('cluster-result');
    recommendationsDiv = document.getElementById('recommendations');
    errorMessage = document.getElementById('error-message');
}

// --- Fungsi untuk Membuat Input Slider ---
function createInterestInputs() {
    if (!inputsContainer || !loadingInputs) return; // Pastikan elemen ada

    // Hapus pesan loading
    loadingInputs.style.display = 'none';
    // inputsContainer.innerHTML = ''; // Kosongkan container sebelum mengisi

    KATEGORI_MINAT.forEach((minat, index) => {
        // Format nama minat agar lebih mudah dibaca
        const namaTampil = minat.replace(/_/g, ' ');

        // Buat elemen div untuk setiap baris input
        const inputGroup = document.createElement('div');
        inputGroup.classList.add('grid', 'grid-cols-1', 'sm:grid-cols-3', 'gap-4', 'items-center');

        // Buat label
        const label = document.createElement('label');
        label.setAttribute('for', `minat-${index}`);
        label.textContent = `${namaTampil}:`;
        label.classList.add('text-gray-700', 'font-medium', 'sm:col-span-1');

        // Container untuk slider dan nilainya
        const sliderContainer = document.createElement('div');
        sliderContainer.classList.add('flex', 'items-center', 'space-x-3', 'sm:col-span-2');

        // Buat slider
        const slider = document.createElement('input');
        slider.setAttribute('type', 'range');
        slider.setAttribute('id', `minat-${index}`);
        slider.setAttribute('name', `minat-${index}`);
        slider.setAttribute('min', '1');
        slider.setAttribute('max', '5');
        slider.setAttribute('value', '3'); // Nilai default
        slider.classList.add('w-full', 'h-2.5', 'bg-gray-200', 'rounded-lg', 'appearance-none', 'cursor-pointer', 'focus:outline-none', 'focus:ring-2', 'focus:ring-offset-2', 'focus:ring-indigo-500');
        slider.dataset.index = index; // Simpan index

        // Buat span untuk menampilkan nilai slider
        const valueSpan = document.createElement('span');
        valueSpan.setAttribute('id', `value-${index}`);
        valueSpan.textContent = slider.value;
        valueSpan.classList.add('text-indigo-700', 'font-bold', 'text-lg', 'slider-value', 'text-center', 'bg-indigo-100', 'rounded-md', 'px-2', 'py-0.5');

        // Tambahkan event listener untuk update nilai saat slider digeser
        slider.addEventListener('input', (event) => {
            valueSpan.textContent = event.target.value;
        });

        // Masukkan slider dan span ke container slider
        sliderContainer.appendChild(slider);
        sliderContainer.appendChild(valueSpan);

        // Masukkan label dan container slider ke dalam group
        inputGroup.appendChild(label);
        inputGroup.appendChild(sliderContainer);

        // Masukkan group ke container utama
        inputsContainer.appendChild(inputGroup);
    });

    // Aktifkan tombol submit setelah input dibuat
    if (submitButton) {
        submitButton.disabled = false;
    }
}

// --- Fungsi untuk Mengirim Data ke API ---
async function getRecommendations() {
    if (!submitButton) return; // Pastikan elemen ada

    // 1. Kumpulkan nilai dari semua slider
    const scores = [];
    let isValid = true;
    for (let i = 0; i < JUMLAH_MINAT; i++) {
        const slider = document.getElementById(`minat-${i}`);
        if (slider) {
            scores.push(parseInt(slider.value, 10)); // Pastikan dikirim sebagai angka
        } else {
            isValid = false;
            console.error(`Slider minat-${i} tidak ditemukan.`);
            break; // Hentikan jika ada slider yang tidak ditemukan
        }
    }

    if (!isValid || scores.length !== JUMLAH_MINAT) {
        showError("Gagal mengumpulkan semua skor minat. Harap refresh halaman.");
        return;
    }

    // 2. Tampilkan loading & sembunyikan hasil/error sebelumnya
    if (loadingSpinner) loadingSpinner.classList.remove('hidden');
    submitButton.disabled = true;
    if (resultsArea) resultsArea.classList.add('hidden');
    if (errorMessage) {
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
    }

    // 3. Buat payload JSON
    const payload = {
        interests: scores
    };

    // 4. Kirim request POST menggunakan Fetch API
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json', // Tambahkan header accept
            },
            body: JSON.stringify(payload) // Ubah objek JS menjadi string JSON
        });

        // Hentikan loading
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
        submitButton.disabled = false;

        // 5. Proses Respons
        const responseData = await response.json(); // Coba parse JSON di semua kasus

        if (response.ok) { // Cek jika status code 200-299
            displayResults(responseData);
        } else {
            // Tangani error dari server (misal: 400 Bad Request, 500 Internal Server Error)
            console.error("Server Error Data:", responseData);
            showError(responseData.error || `Terjadi kesalahan saat menghubungi server (Status: ${response.status}).`);
        }

    } catch (error) {
        // Tangani error jaringan atau error lainnya
        console.error("Fetch error:", error);
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
        submitButton.disabled = false;
        showError("Tidak dapat terhubung ke server. Pastikan server backend berjalan dan URL API benar.");
    }
}

// --- Fungsi untuk Menampilkan Hasil ---
function displayResults(result) {
    if (!resultsArea || !clusterResult || !recommendationsDiv || !errorMessage) return; // Pastikan elemen ada

    resultsArea.classList.remove('hidden'); // Tampilkan area hasil
    errorMessage.classList.add('hidden'); // Sembunyikan pesan error

    clusterResult.textContent = `Berdasarkan minatmu, kamu cocok dengan kelompok Cluster ${result.cluster}.`;

    // Kosongkan rekomendasi sebelumnya
    recommendationsDiv.innerHTML = '';

    if (result.rekomendasi && result.rekomendasi.length > 0) {
        const title = document.createElement('p');
        title.classList.add('text-lg', 'font-semibold', 'text-gray-800', 'mb-2');
        title.textContent = 'Ekstrakurikuler yang mungkin cocok:';
        recommendationsDiv.appendChild(title);

        const list = document.createElement('ul');
        list.classList.add('list-none', 'space-y-2'); // Menggunakan list tanpa bullet point
        result.rekomendasi.forEach(ekskul => {
            const listItem = document.createElement('li');
            listItem.classList.add('p-3', 'bg-white', 'rounded-md', 'shadow-sm', 'border', 'border-gray-200', 'flex', 'items-center');

            // Tambahkan ikon sederhana (misalnya bintang)
            const icon = document.createElement('span');
            icon.classList.add('text-yellow-500', 'mr-3', 'text-xl');
            icon.innerHTML = '&#9733;'; // Kode HTML untuk bintang

            const text = document.createElement('span');
            text.textContent = ekskul;
            text.classList.add('text-gray-900', 'font-medium');

            listItem.appendChild(icon);
            listItem.appendChild(text);
            list.appendChild(listItem);
        });
        recommendationsDiv.appendChild(list);
    } else {
        recommendationsDiv.textContent = "Hmm, sepertinya belum ada rekomendasi spesifik untuk kelompok minat ini.";
        recommendationsDiv.classList.add('text-center', 'text-gray-600', 'italic');
    }
}

// --- Fungsi untuk Menampilkan Error ---
function showError(message) {
    if (!resultsArea || !errorMessage) return; // Pastikan elemen ada

    resultsArea.classList.add('hidden'); // Sembunyikan area hasil
    errorMessage.classList.remove('hidden'); // Tampilkan area error
    errorMessage.textContent = `Oops! Terjadi Kesalahan: ${message}`;
}

// --- Event Listener ---
// Pastikan DOM siap sebelum menjalankan kode yang mengakses elemen
document.addEventListener('DOMContentLoaded', () => {
    initializeDOMReferences(); // Ambil referensi elemen
    createInterestInputs(); // Buat input slider

    // Tambahkan event listener ke tombol submit hanya jika tombolnya ada
    if (submitButton) {
        submitButton.addEventListener('click', getRecommendations);
    } else {
        console.error("Tombol submit tidak ditemukan!");
    }
});