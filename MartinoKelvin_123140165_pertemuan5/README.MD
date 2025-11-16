# Sistem Manajemen Perpustakaan Sederhana

**Nama:** Martino Kelvin

**NIM:** 123140165

**Mata Kuliah:** Pemrograman Python - Pertemuan 

## 📚 Deskripsi Program

Sistem Manajemen Perpustakaan Sederhana adalah aplikasi berbasis Python yang mengimplementasikan konsep Object-Oriented Programming (OOP) untuk mengelola koleksi perpustakaan. Program ini dapat menangani berbagai jenis item perpustakaan seperti buku dan majalah.

### ✨ Fitur Utama

1. **Manajemen Item Perpustakaan**
   * Menambahkan buku dan majalah ke koleksi
   * Menampilkan daftar semua item
   * Mencari item berdasarkan judul atau ID
2. **Sistem Peminjaman**
   * Meminjam item dari perpustakaan
   * Mengembalikan item yang dipinjam
   * Tracking status ketersediaan item
3. **Statistik Perpustakaan**
   * Total koleksi (buku dan majalah)
   * Jumlah item tersedia
   * Total peminjaman

---

## 🎯 Implementasi Konsep OOP

### 1. Abstract Class dan Inheritance (30%)

* **`LibraryItem`** (Abstract Base Class)
  * Menjadi blueprint untuk semua item perpustakaan
  * Mendefinisikan abstract methods: `display_info()` dan `get_category()`
  * Memiliki atribut dan method umum untuk semua item
* **`Book`** dan **`Magazine`** (Subclasses)
  * Mewarisi dari `LibraryItem`
  * Mengimplementasikan abstract methods sesuai karakteristik masing-masing
  * Menambahkan atribut spesifik (author/ISBN untuk buku, publisher/issue untuk majalah)

### 2. Encapsulation (25%)

* **Private Attributes** (prefix `__`)
  * `__item_id`, `__author`, `__isbn`, `__publisher`, dll
  * Tidak dapat diakses langsung dari luar class
* **Protected Attributes** (prefix `_`)
  * `_title`, `_year`, `_is_available`
  * Dapat diakses oleh subclass
* **Property Decorators**
  * `@property` untuk getter methods
  * `@setter` untuk setter methods dengan validasi
  * Contoh: property `title` dengan validasi tidak boleh kosong

### 3. Polymorphism (20%)

* **Method Overriding**
  * Method `display_info()` diimplementasikan berbeda di `Book` dan `Magazine`
  * Method `get_category()` mengembalikan nilai berbeda sesuai jenis item
  * Duck typing: semua objek `LibraryItem` dapat dipanggil method yang sama

### 4. Abstraction

* Menggunakan `ABC` (Abstract Base Class) dari module `abc`
* Memaksa subclass untuk mengimplementasikan method tertentu
* Menyembunyikan kompleksitas implementasi dari user

---

## 🏗️ Struktur Class

```
LibraryItem (Abstract)          → library_item.py
├── Book                        → book.py
└── Magazine                    → magazine.py

Library (Composition)           → library.py
└── List[LibraryItem]
```

### Class Diagram

```
┌─────────────────────────┐
│   LibraryItem (ABC)     │  ← library_item.py
├─────────────────────────┤
│ - __item_id: str        │
│ - _title: str           │
│ - _year: int            │
│ - _is_available: bool   │
├─────────────────────────┤
│ + display_info()* ──────┼────► Abstract Method
│ + get_category()*       │
│ + borrow(): bool        │
│ + return_item(): bool   │
└──────────┬──────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───────┐ ┌──▼───────────┐
│   Book    │ │   Magazine   │  ← book.py / magazine.py
├───────────┤ ├──────────────┤
│- __author │ │- __publisher │
│- __isbn   │ │- __issue_no  │
│- __pages  │ │- __month     │
└───────────┘ └──────────────┘

┌─────────────────────────┐
│       Library           │  ← library.py
├─────────────────────────┤
│ - __name: str           │
│ - __items: List         │
│ - __total_borrowed: int │
├─────────────────────────┤
│ + add_item()            │
│ + display_all_items()   │
│ + search_by_title()     │
│ + search_by_id()        │
│ + borrow_item()         │
│ + return_item()         │
│ + get_statistics()      │
└─────────────────────────┘
```

---

## 📁 Struktur File

```
[NAMA]_[NIM]_pertemuan5/
│
├── main.py                 # Entry point program (REQUIRED)
├── library_item.py         # Abstract base class LibraryItem (REQUIRED)
├── book.py                 # Class Book (subclass) (REQUIRED)
├── magazine.py             # Class Magazine (subclass) (REQUIRED)
├── library.py              # Class Library untuk manajemen (REQUIRED)
├── test_library.py         # Unit tests (OPTIONAL - bonus point)
├── dvd.py                  # Contoh extensibility (OPTIONAL - bonus point)
├── requirements.txt        # Dependencies (OPTIONAL)
├── .gitignore              # Git ignore file (OPTIONAL)
├── QUICKSTART.md           # Quick start guide (OPTIONAL)
└── README.md               # Dokumentasi (REQUIRED)
```

### Penjelasan File

| File                 | Deskripsi                                                  | Status             |
| -------------------- | ---------------------------------------------------------- | ------------------ |
| `main.py`          | Program utama yang menjalankan demo sistem                 | **REQUIRED** |
| `library_item.py`  | Abstract base class untuk semua item perpustakaan          | **REQUIRED** |
| `book.py`          | Class untuk buku dengan atribut author, ISBN, pages        | **REQUIRED** |
| `magazine.py`      | Class untuk majalah dengan atribut publisher, issue, month | **REQUIRED** |
| `library.py`       | Class untuk mengelola koleksi perpustakaan                 | **REQUIRED** |
| `test_library.py`  | Unit testing dengan unittest (bonus point)                 | **OPTIONAL** |
| `dvd.py`           | Contoh extensibility - menambah item type baru             | **OPTIONAL** |
| `requirements.txt` | List dependencies Python                                   | **OPTIONAL** |
| `.gitignore`       | File untuk mengabaikan cache/temp files                    | **OPTIONAL** |

## 🚀 Cara Menjalankan Program

### Prasyarat

* Python 3.x terinstall
* Terminal/Command Prompt

### Langkah-langkah

1. **Clone atau Download File**

   ```bash
   git clone https://github.com/username/pemrograman_python_itera_[NIM]
   cd [NAMA]_[NIM]_pertemuan5
   ```
2. **Pastikan Semua File Ada**

   ```bash
   ls -la
   # Harus ada: main.py, library_item.py, book.py, magazine.py, library.py
   ```
3. **Jalankan Program**

   ```bash
   python main.py
   ```
4. **Jalankan Unit Tests (Optional)**

   ```bash
   python test_library.py
   ```

   Atau menggunakan unittest discovery:

   ```bash
   python -m unittest test_library.py -v
   ```
5. **Test Extensibility dengan DVD (Optional)**

   ```bash
   python dvd.py
   ```

   Mendemonstrasikan bagaimana mudahnya menambah item type baru

---

## 📸 Screenshot Hasil Running

### 1. Menambahkan Item ke Perpustakaan

```
============================================================
  SISTEM MANAJEMEN PERPUSTAKAAN SEDERHANA
  Implementasi OOP dengan Python
============================================================

✓ Item 'Pemrograman Python' berhasil ditambahkan ke perpustakaan
✓ Item 'Machine Learning Fundamentals' berhasil ditambahkan ke perpustakaan
✓ Item 'Data Science dengan Python' berhasil ditambahkan ke perpustakaan
✓ Item 'Tech Monthly' berhasil ditambahkan ke perpustakaan
✓ Item 'Science Today' berhasil ditambahkan ke perpustakaan
```

### 2. Daftar Semua Item

```
============================================================
  DAFTAR KOLEKSI PERPUSTAKAAN ITERA
============================================================
Total item: 5 | Tersedia: 5
============================================================

1. [✓] Buku: Pemrograman Python
   ID: B001 | Tahun: 2024

2. [✓] Buku: Machine Learning Fundamentals
   ID: B002 | Tahun: 2023

3. [✓] Buku: Data Science dengan Python
   ID: B003 | Tahun: 2024

4. [✓] Majalah: Tech Monthly
   ID: M001 | Tahun: 2024

5. [✓] Majalah: Science Today
   ID: M002 | Tahun: 2024
```

### 3. Detail Item (Polymorphism)

```
╔══════════════════════════════════════════╗
║            INFORMASI BUKU                ║
╠══════════════════════════════════════════╣
║ ID       : B001                          ║
║ Judul    : Pemrograman Python            ║
║ Penulis  : John Doe                      ║
║ Tahun    : 2024                          ║
║ ISBN     : 978-1234567890                ║
║ Halaman  : 350                           ║
║ Status   : ✓ Tersedia                    ║
╚══════════════════════════════════════════╝
```

### 4. Pencarian Item

```
============================================================
  PENCARIAN BERDASARKAN JUDUL: 'Python'
============================================================
✓ Ditemukan: Buku - Pemrograman Python (Tersedia)
✓ Ditemukan: Buku - Data Science dengan Python (Tersedia)
```

### 5. Peminjaman Item

```
============================================================
  SIMULASI PEMINJAMAN
============================================================
✓ Berhasil meminjam: Pemrograman Python
✓ Berhasil meminjam: Tech Monthly
```

### 6. Statistik Perpustakaan

```
==================================================
  STATISTIK PERPUSTAKAAN ITERA
==================================================
Total Koleksi       : 5 item
  - Buku            : 3 item
  - Majalah         : 2 item
Tersedia            : 3 item
Sedang Dipinjam     : 2 item
Total Peminjaman    : 2 kali
==================================================
```

---

## 📝 Penjelasan Kode

### 1. library_item.py - Abstract Class

```python
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    # Menggunakan @abstractmethod untuk memaksa implementasi di subclass
    @abstractmethod
    def display_info(self) -> str:
        pass
```

### 2. book.py & magazine.py - Inheritance

```python
from library_item import LibraryItem

class Book(LibraryItem):
    # Mewarisi semua atribut dan method dari LibraryItem
    def __init__(self, item_id, title, year, author, isbn, pages):
        super().__init__(item_id, title, year)  # Call parent constructor
        self.__author = author
```

### 3. Property Decorator - Encapsulation

```python
@property
def title(self) -> str:
    """Getter untuk title"""
    return self._title

@title.setter
def title(self, value: str):
    """Setter dengan validasi"""
    if not value or len(value.strip()) == 0:
        raise ValueError("Judul tidak boleh kosong")
    self._title = value
```

### 4. Method Overriding - Polymorphism

```python
# Di book.py
def display_info(self) -> str:
    # Implementasi khusus untuk buku
    return f"Info Buku: {self.title}..."

# Di magazine.py
def display_info(self) -> str:
    # Implementasi khusus untuk majalah
    return f"Info Majalah: {self.title}..."
```

### 5. library.py - Composition

```python
class Library:
    def __init__(self, name: str):
        self.__items: List[LibraryItem] = []  # Composition
  
    def add_item(self, item: LibraryItem):
        # Menerima semua jenis LibraryItem (Book/Magazine)
        self.__items.append(item)
```

---

## 🎓 Konsep OOP yang Diterapkan

| Konsep                       | Implementasi                                      | File & Lokasi                                            |
| ---------------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| **Abstraction**        | Abstract Base Class `LibraryItem`               | `library_item.py`(baris 11-117)                        |
| **Inheritance**        | `Book`dan `Magazine`extends `LibraryItem`   | `book.py`(baris 10)`<br>magazine.py`(baris 10)       |
| **Encapsulation**      | Private (`__`) dan Protected (`_`) attributes | Semua file class                                         |
| **Polymorphism**       | Method overriding `display_info()`              | `book.py`(baris 50-69)`<br>magazine.py`(baris 50-69) |
| **Property Decorator** | `@property`dan `@setter`                      | `library_item.py`(baris 32-65)                         |
| **Composition**        | Library berisi List[LibraryItem]                  | `library.py`(baris 26)                                 |
| **Type Hints**         | Anotasi tipe pada parameters dan return           | Semua file                                               |

---

## 💡 Fitur Tambahan

1. **Type Hints** : Menggunakan typing untuk meningkatkan readability
2. **Docstrings** : Dokumentasi lengkap pada setiap class dan method
3. **Error Handling** : Validasi input dan pengecekan kondisi
4. **Clean Code** : Penamaan variabel yang jelas dan struktur yang terorganisir
5. **User-Friendly Output** : Format output yang mudah dibaca dengan simbol dan border
6. **Modular Design** : Pemisahan file berdasarkan tanggung jawab (Separation of Concerns)
7. **Unit Testing** : Test coverage untuk validasi fungsi (optional - bonus point)
8. **Extensibility** : Mudah menambahkan item type baru (contoh: DVD) tanpa mengubah kode existing

---

## 🔍 Keunggulan Struktur Multi-File

### Advantages:

1. **Maintainability** : Mudah di-maintain karena setiap class di file terpisah
2. **Readability** : Lebih mudah dibaca dan dipahami
3. **Reusability** : Class bisa di-import dan digunakan di project lain
4. **Testability** : Mudah untuk membuat unit test per module
5. **Collaboration** : Memudahkan kerja tim (menghindari merge conflict)
6. **Scalability** : Mudah ditambahkan class baru tanpa mengubah file lain

### Best Practices:

* Setiap file fokus pada satu tanggung jawab (Single Responsibility Principle)
* Import hanya yang diperlukan
* Gunakan relative imports untuk module dalam project yang sama
* Dokumentasi yang jelas di setiap file

### SOLID Principles yang Diterapkan:

* **S**ingle Responsibility: Setiap class punya satu tanggung jawab
* **O**pen/Closed: Sistem terbuka untuk extension (lihat dvd.py), tertutup untuk modification
* **L**iskov Substitution: Semua subclass bisa menggantikan parent class
* **I**nterface Segregation: Abstract methods yang focused dan specific
* **D**ependency Inversion: Library depends on abstraction (LibraryItem), bukan concrete classes

---

## 📚 Referensi

* [Python Official Documentation - OOP](https://docs.python.org/3/tutorial/classes.html)
* [Real Python - OOP in Python](https://realpython.com/python3-object-oriented-programming/)
* [Python ABC Module](https://docs.python.org/3/library/abc.html)

---

## 👨‍💻 Author

**Martino Kelvin**

NIM: 123140165

Program Studi: Teknik Informatika

Institut Teknologi Sumatera

---

## 📄 Lisensi

Program ini dibuat untuk keperluan akademik Praktikum Pemrograman Python - Pertemuan 5

---

## 🎁 Bonus Points (Opsional)

Untuk mendapatkan nilai tambahan, Anda bisa menambahkan:

1. **Unit Testing** (`test_library.py`)
   * ✅ Test coverage untuk semua fungsi utama
   * ✅ Test untuk encapsulation dan validation
   * ✅ Automated testing dengan unittest
2. **Extensibility Demo** (`dvd.py`)
   * ✅ Mendemonstrasikan Open/Closed Principle
   * ✅ Mudah menambah item type baru
   * ✅ Tidak perlu modifikasi kode existing
3. **Diagram Class yang Lengkap**
   * ✅ Visual representation dari struktur OOP
   * ✅ Menunjukkan relationships antar class
4. **Dokumentasi yang Excellent**
   * ✅ README yang comprehensive
   * ✅ Docstrings di semua class dan method
   * ✅ Comments yang informatif
5. **Clean Code Practices**
   * ✅ Type hints untuk semua function
   * ✅ Proper naming conventions
   * ✅ Modular design dengan separation of concerns

---

**Catatan:** Ganti placeholder `[NAMA_ANDA]`, `[NIM_ANDA]`, dll dengan informasi Anda sebelum submit.

---

## 📦 Semua File Yang Tersedia

### Files REQUIRED (Wajib)

1. ✅ `main.py` - Program utama
2. ✅ `library_item.py` - Abstract base class
3. ✅ `book.py` - Class Book
4. ✅ `magazine.py` - Class Magazine
5. ✅ `library.py` - Class Library
6. ✅ `README.md` - Dokumentasi utama

### Files OPTIONAL (Bonus)

7. 🎁 `test_library.py` - Unit tests (bonus +5%)
8. 🎁 `dvd.py` - Contoh extensibility (bonus +3%)
9. 🎁 `demo_custom.py` - Custom demo examples
10. 🎁 `QUICKSTART.md` - Quick start guide
11. 🎁 `SUBMISSION_CHECKLIST.md` - Checklist lengkap
12. 🎁 `requirements.txt` - Dependencies
13. 🎁 `.gitignore` - Git ignore

### Total: 13 Files

* **Minimum required:** 6 files (main + 4 classes + README)
* **Recommended:** 10+ files untuk bonus points

---

## 🎯 Quick Links

* 📖 [Quick Start Guide](https://claude.ai/chat/QUICKSTART.md) - Panduan cepat memulai
* ✅ [Submission Checklist](https://claude.ai/chat/SUBMISSION_CHECKLIST.md) - Checklist sebelum submit
* 🧪 Run tests: `python test_library.py`
* 🎨 Custom demo: `python demo_custom.py`
* 📚 Full documentation: Lihat README ini
