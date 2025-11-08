
"""
Program Pengelolaan Data Nilai Mahasiswa
Martino Kelvin — NIM 123140165 (contoh pengisian)

Fitur:
- Data awal (≥5) berupa list[dict]
- Hitung nilai akhir: 30% UTS + 40% UAS + 30% Tugas
- Tentukan grade (A/B/C/D/E)
- Tampilkan tabel rapi
- Cari nilai tertinggi & terendah
- Tambah data mahasiswa via input
- Filter berdasarkan grade
- Hitung rata-rata kelas

Penilaian:
- Fungsi modular, docstring, typing, PEP8 ringkas.
"""

from __future__ import annotations
from typing import List, Dict, Tuple

Mahasiswa = Dict[str, object]  
mahasiswa: List[Mahasiswa] = [
    {"nama": "Martino Kelvin", "nim": "123140165", "nilai_uts": 82, "nilai_uas": 88, "nilai_tugas": 90},
    {"nama": "Diva Prameswari", "nim": "123140201", "nilai_uts": 74, "nilai_uas": 79, "nilai_tugas": 80},
    {"nama": "Aji Pratama",    "nim": "123140172", "nilai_uts": 65, "nilai_uas": 60, "nilai_tugas": 70},
    {"nama": "Ikhsan F.",      "nim": "123140190", "nilai_uts": 55, "nilai_uas": 58, "nilai_tugas": 60},
    {"nama": "Prima A.",       "nim": "123140210", "nilai_uts": 92, "nilai_uas": 90, "nilai_tugas": 95},
]



def hitung_nilai_akhir(m: Mahasiswa) -> float:
    """Hitung nilai akhir: 30% UTS + 40% UAS + 30% Tugas."""
    uts = float(m["nilai_uts"])
    uas = float(m["nilai_uas"])
    tugas = float(m["nilai_tugas"])
    return round(0.30 * uts + 0.40 * uas + 0.30 * tugas, 2)


def tentukan_grade(nilai_akhir: float) -> str:
    """Mapping nilai akhir ke grade huruf."""
    if nilai_akhir >= 80:
        return "A"
    elif nilai_akhir >= 70:
        return "B"
    elif nilai_akhir >= 60:
        return "C"
    elif nilai_akhir >= 50:
        return "D"
    else:
        return "E"


def format_tabel(data: List[Mahasiswa]) -> str:
    """Bangun string tabel rapi tanpa library eksternal."""
    headers = ["No", "NIM", "Nama", "UTS", "UAS", "Tugas", "Akhir", "Grade"]
    rows = []

    for i, m in enumerate(data, start=1):
        akhir = hitung_nilai_akhir(m)
        grade = tentukan_grade(akhir)
        rows.append([
            str(i),
            str(m["nim"]),
            str(m["nama"]),
            f'{float(m["nilai_uts"]):.2f}',
            f'{float(m["nilai_uas"]):.2f}',
            f'{float(m["nilai_tugas"]):.2f}',
            f"{akhir:.2f}",
            grade,
        ])

    # hitung lebar kolom
    col_widths = [len(h) for h in headers]
    for row in rows:
        for j, cell in enumerate(row):
            col_widths[j] = max(col_widths[j], len(cell))

    def fmt_row(row_vals: List[str]) -> str:
        return " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(row_vals))

    line = "-+-".join("-" * w for w in col_widths)
    out = [fmt_row(headers), line]
    out += [fmt_row(r) for r in rows]
    return "\n".join(out)


def tampilkan_data(data: List[Mahasiswa]) -> None:
    """Cetak tabel data mahasiswa beserta nilai akhir & grade."""
    if not data:
        print("Tidak ada data.")
        return
    print(format_tabel(data))


def cari_tertinggi_terendah(data: List[Mahasiswa]) -> Tuple[Mahasiswa, Mahasiswa]:
    """Kembalikan tuple (maks, min) berdasarkan nilai akhir."""
    if not data:
        raise ValueError("Data kosong.")
    ter_maks = max(data, key=hitung_nilai_akhir)
    ter_min = min(data, key=hitung_nilai_akhir)
    return ter_maks, ter_min


def filter_berdasarkan_grade(data: List[Mahasiswa], grade: str) -> List[Mahasiswa]:
    """Filter mahasiswa yang grade-nya == grade (case-insensitive)."""
    g = grade.upper().strip()
    return [m for m in data if tentukan_grade(hitung_nilai_akhir(m)) == g]


def rata_rata_kelas(data: List[Mahasiswa]) -> float:
    """Rata-rata nilai akhir kelas."""
    if not data:
        return 0.0
    total = sum(hitung_nilai_akhir(m) for m in data)
    return round(total / len(data), 2)


def cari_by_nim(data: List[Mahasiswa], nim: str) -> Mahasiswa | None:
    """Cari mahasiswa berdasarkan NIM, kembalikan dict atau None."""
    nim = nim.strip()
    for m in data:
        if str(m["nim"]) == nim:
            return m
    return None


# --- Input Data ---
def input_float(prompt: str, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Helper untuk input nilai numerik dengan validasi sederhana."""
    while True:
        try:
            val = float(input(prompt))
            if val < min_val or val > max_val:
                print(f"Nilai harus di rentang {min_val}–{max_val}.")
                continue
            return val
        except ValueError:
            print("Input harus berupa angka.")


def tambah_mahasiswa(data: List[Mahasiswa]) -> None:
    """Tambahkan data mahasiswa melalui input CLI."""
    print("\n=== Tambah Data Mahasiswa ===")
    nim = input("NIM         : ").strip()
    if nim == "":
        print("NIM tidak boleh kosong.")
        return
    if cari_by_nim(data, nim):
        print("NIM sudah terdaftar.")
        return

    nama = input("Nama        : ").strip()
    if nama == "":
        print("Nama tidak boleh kosong.")
        return

    uts = input_float("Nilai UTS   : ")
    uas = input_float("Nilai UAS   : ")
    tugas = input_float("Nilai Tugas : ")

    data.append({
        "nama": nama,
        "nim": nim,
        "nilai_uts": uts,
        "nilai_uas": uas,
        "nilai_tugas": tugas,
    })
    print("Data berhasil ditambahkan.\n")


# --- Menu CLI ---
def tampilkan_menu() -> None:
    print("""
=============================
  Pengelolaan Nilai Mahasiswa
=============================
1. Tampilkan semua data
2. Tambah data mahasiswa
3. Cari nilai tertinggi / terendah
4. Filter berdasarkan grade
5. Hitung rata-rata kelas
6. Cari mahasiswa (berdasarkan NIM)
0. Keluar
""")


def main() -> None:
    while True:
        tampilkan_menu()
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            tampilkan_data(mahasiswa)

        elif pilih == "2":
            tambah_mahasiswa(mahasiswa)

        elif pilih == "3":
            try:
                ter_maks, ter_min = cari_tertinggi_terendah(mahasiswa)
                print("\n— Nilai Tertinggi —")
                tampilkan_data([ter_maks])
                print("\n— Nilai Terendah —")
                tampilkan_data([ter_min])
                print()
            except ValueError as e:
                print(f"Error: {e}\n")

        elif pilih == "4":
            g = input("Masukkan grade (A/B/C/D/E): ").strip().upper()
            if g not in {"A", "B", "C", "D", "E"}:
                print("Grade tidak valid.\n")
            else:
                hasil = filter_berdasarkan_grade(mahasiswa, g)
                if not hasil:
                    print(f"Tidak ada mahasiswa dengan grade {g}.\n")
                else:
                    print(f"\n— Mahasiswa dengan grade {g} —")
                    tampilkan_data(hasil)
                    print()

        elif pilih == "5":
            avg = rata_rata_kelas(mahasiswa)
            print(f"Rata-rata nilai akhir kelas: {avg:.2f}\n")

        elif pilih == "6":
            nim = input("Masukkan NIM: ").strip()
            m = cari_by_nim(mahasiswa, nim)
            if m:
                tampilkan_data([m])
                print()
            else:
                print("Mahasiswa tidak ditemukan.\n")

        elif pilih == "0":
            print("Terima kasih. Keluar...")
            break
        else:
            print("Pilihan tidak dikenal.\n")


if __name__ == "__main__":
    main()
