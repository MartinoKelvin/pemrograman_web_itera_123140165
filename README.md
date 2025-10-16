**Tugas Praktikum – Mata Kuliah Pemrograman Aplikasi Web**

**📘 Penjelasan Singkat**

Aplikasi ini merupakan proyek praktikum untuk mata kuliah Pemrograman Aplikasi Web.
Tujuan aplikasi adalah membantu mahasiswa dalam mengelola dan memantau tugas perkuliahan agar lebih terorganisir.

Aplikasi ini bersifat interaktif, mudah digunakan, serta menyimpan data secara lokal menggunakan localStorage tanpa perlu koneksi ke server.
Dengan aplikasi ini, pengguna dapat menambah tugas, menandai tugas yang sudah selesai, menghapus tugas yang sudah tidak relevan, dan memfilter daftar tugas sesuai kebutuhan.

**⚙️ Cara Menjalankan Aplikasi**

Clone atau unduh repositori ini:
```bash
git clone https://github.com/<username-kamu>/manajemen-tugas-mahasiswa.git

```
Buka folder proyek:
```bash
cd manajemen-tugas-mahasiswa

```
Jalankan aplikasi dengan membuka file index.html di browser (Chrome, Edge, Firefox, dsb).

Tidak perlu server atau setup tambahan — aplikasi berjalan langsung di browser karena menggunakan localStorage.

**🧩 Daftar Fitur yang Telah Diimplementasikan**<br>
**Fitur	Deskripsi**<br>
➕ Tambah Tugas	Pengguna dapat menambahkan tugas baru dengan data: nama tugas, mata kuliah, dan deadline. <br>
🧠 Validasi Form	Form melakukan pengecekan agar semua input wajib diisi dan tanggal yang dimasukkan valid. <br>
✅ Tandai Tugas Selesai	Pengguna dapat menandai tugas sebagai “selesai” atau “belum selesai”.<br>
❌ Hapus Tugas	Menghapus tugas yang sudah tidak diperlukan dari daftar.<br>
🔍 Filter/Pencarian Tugas	Menyaring tugas berdasarkan status (selesai/belum) atau berdasarkan mata kuliah.<br>
📊 Statistik Tugas	Menampilkan jumlah total tugas dan jumlah yang sudah diselesaikan.<br>
💾 Penyimpanan Lokal (localStorage)	Semua data tugas disimpan secara lokal di browser, sehingga tetap tersimpan walau halaman direfresh.<br>
🎨 Desain Responsif	Menggunakan Tailwind CSS agar tampilan tetap rapi dan nyaman di berbagai ukuran layar.<br>

**🖼️ Screenshot Aplikasi**

**Form tambah tugas dengan validasi input**
<img width="918" height="517" alt="image" src="https://github.com/user-attachments/assets/bbe1ae77-5e1e-4c63-a360-1e6449804b1c" />

**Filter tugas**
<img width="901" height="168" alt="image" src="https://github.com/user-attachments/assets/0a212dc1-22ad-4eb0-b196-d18bd9c5e5d6" />

**Daftar tugas dengan tombol tandai & hapus**
<img width="916" height="289" alt="image" src="https://github.com/user-attachments/assets/61d3370e-76ed-4d66-9a14-8e0aba0c6c28" />

**tampilan statistik jumlah selesai dan belum selesai**
<img width="915" height="189" alt="image" src="https://github.com/user-attachments/assets/6154ffa2-dae5-4991-86bd-05a9c7af3e75" />

**🧠 Penjelasan Teknis**
**1️⃣ Penyimpanan Data (localStorage)** <br>

Aplikasi menggunakan Web Storage API (localStorage) untuk menyimpan data tugas.
Setiap kali pengguna menambah, mengedit, atau menghapus tugas, data disimpan ulang agar tetap sinkron.
```js
Menyimpan data:
localStorage.setItem('tasks', JSON.stringify(tasks));

Mengambil data:
const tasks = JSON.parse(localStorage.getItem('tasks')) || [];

```
Data disimpan dalam format JSON agar mudah diubah kembali ke array JavaScript.

localStorage memastikan data tetap tersimpan meskipun browser direfresh atau ditutup.

**2️⃣ Validasi Form** <br>

Sebelum menambah tugas, aplikasi memeriksa apakah semua input valid:

```js
if (!name || !course || !deadline) { 
  alert("Semua field wajib diisi!"); 
  return; 
} 


```
Validasi meliputi:

Nama tugas dan mata kuliah tidak boleh kosong

Deadline harus berisi tanggal yang valid

Input akan dicegah masuk ke daftar bila tidak memenuhi aturan

**🧰 Teknologi yang Digunakan** <br>
**Teknologi	Kegunaan** <br>
HTML5	Struktur dan elemen utama halaman <br>
Tailwind CSS (CDN)	Styling cepat dan responsif <br>
JavaScript (Vanilla)	Logika aplikasi (CRUD, filter, validasi, penyimpanan) <br>
localStorage API	Menyimpan data secara lokal di browser <br>

**👨‍🎓 Identitas Mahasiswa** <br>
Informasi	Keterangan <br> 
Nama	Martino Kelvin <br>
NIM	123140165 <br>
Program Studi	Teknik Informatika <br>
Mata Kuliah	Pemrograman Aplikasi Web RA <br>
Institusi	Institut Teknologi Sumatera (ITERA) <br>

**📄 Lisensi** <br>

Proyek ini dibuat untuk keperluan akademik dan pembelajaran.
Diperbolehkan untuk digunakan, dimodifikasi, atau dikembangkan lebih lanjut untuk tujuan edukatif.





