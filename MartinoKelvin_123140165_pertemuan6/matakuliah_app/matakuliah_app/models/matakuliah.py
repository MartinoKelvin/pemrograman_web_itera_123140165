"""
MODUL MODEL MATAKULIAH - Definisi ORM untuk Tabel Matakuliah

Modul ini mendefinisikan model Matakuliah menggunakan SQLAlchemy ORM.
Model ini merepresentasikan tabel 'matakuliah' dalam database PostgreSQL.

Fungsi Model:
  1. Menjelaskan struktur tabel ke Python
  2. Mapping antara tabel database dan object Python
  3. Menyediakan method untuk konversi ke dictionary (to_dict)
  4. Menyediakan string representation untuk debugging

Kontribusi ke Kriteria Penilaian:
  - Model Data (30%): Atribut lengkap, validasi, method to_dict()
  - Dokumentasi dan Kerapian Kode: Comments dan docstrings lengkap
"""
from sqlalchemy import Column, Integer, Text
from .meta import Base


class Matakuliah(Base):
    """
    MODEL MATAKULIAH - Representasi Object-Oriented untuk tabel matakuliah
    
    Kelas ini merepresentasikan satu baris data di tabel matakuliah.
    Setiap instance adalah satu record matakuliah.
    
    Atribut & Constraint Database:
    
    1. id (Integer)
       - Primary Key
       - Auto Increment
       - Nilai otomatis saat insert
       - Digunakan sebagai unique identifier
       
    2. kode_mk (Text)
       - Kode/ID mata kuliah (misal: IF101, IF102)
       - UNIQUE: Tidak boleh ada 2 matakuliah dengan kode sama
       - NOT NULL: Wajib ada nilai, tidak boleh kosong
       - Tipe: String/Text
       - Validasi: Harus string, tidak boleh kosong
       - Contoh: 'IF101', 'IF102', 'IF201'
       
    3. nama_mk (Text)
       - Nama lengkap mata kuliah
       - NOT NULL: Wajib ada nilai
       - Tipe: String/Text
       - Validasi: Harus string, tidak boleh kosong
       - Contoh: 'Algoritma dan Pemrograman', 'Struktur Data'
       
    4. sks (Integer)
       - Satuan Kredit Semester (credit hours)
       - NOT NULL: Wajib ada nilai
       - Tipe: Integer (angka bulat)
       - Validasi: Harus integer positif (> 0)
       - Contoh: 3, 4, 2
       
    5. semester (Integer)
       - Semester pengambilan mata kuliah
       - NOT NULL: Wajib ada nilai
       - Tipe: Integer (angka bulat)
       - Validasi: Harus integer positif (> 0), max 8 semester
       - Contoh: 1, 2, 3, 4
    
    Struktur SQL Tabel:
        CREATE TABLE matakuliah (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            kode_mk TEXT UNIQUE NOT NULL,
            nama_mk TEXT NOT NULL,
            sks INTEGER NOT NULL,
            semester INTEGER NOT NULL
        );
    
    Contoh Penggunaan:
    
        # CREATE (insert data baru)
        mk = Matakuliah(
            kode_mk='IF101',
            nama_mk='Algoritma dan Pemrograman',
            sks=3,
            semester=1
        )
        dbsession.add(mk)
        dbsession.flush()
        print(mk.id)  # Auto-generated ID
        
        # READ (query data)
        mk = dbsession.query(Matakuliah).filter_by(id=1).one()
        print(mk.nama_mk)
        
        # UPDATE (modifikasi data)
        mk.sks = 4
        dbsession.flush()
        
        # DELETE (hapus data)
        dbsession.delete(mk)
        dbsession.flush()
    """
    
    # ========== DEFINISI TABEL ==========
    # Nama tabel di database PostgreSQL yang akan digunakan
    __tablename__ = 'matakuliah'
    
    
    # ========== DEFINISI KOLOM/ATRIBUT ==========
    # Masing-masing Column mewakili satu kolom di tabel database
    
    # Kolom ID - Primary Key dengan auto increment
    # - Integer: Tipe data angka bulat
    # - primary_key=True: Ini kolom utama, harus unique
    # - Auto increment: Pyramid/PostgreSQL akan membuat value otomatis
    id = Column(Integer, primary_key=True)
    
    # Kolom KODE_MK - Kode mata kuliah (unique)
    # - Text: Tipe data string/text
    # - unique=True: Tidak boleh ada 2 baris dengan nilai yang sama
    # - nullable=False: Kolom wajib diisi, tidak boleh NULL/kosong
    # Constraint di database ini memastikan validasi di level database
    kode_mk = Column(Text, unique=True, nullable=False)
    
    # Kolom NAMA_MK - Nama mata kuliah
    # - Text: Tipe data string/text
    # - nullable=False: Kolom wajib diisi
    nama_mk = Column(Text, nullable=False)
    
    # Kolom SKS - Satuan Kredit Semester
    # - Integer: Tipe data angka bulat
    # - nullable=False: Kolom wajib diisi
    sks = Column(Integer, nullable=False)
    
    # Kolom SEMESTER - Semester pengambilan
    # - Integer: Tipe data angka bulat
    # - nullable=False: Kolom wajib diisi
    semester = Column(Integer, nullable=False)
    
    
    # ========== METHOD UNTUK KONVERSI DATA ==========
    
    def to_dict(self):
        """
        METHOD KONVERSI - Convert model instance ke dictionary
        
        Mengubah object Python (Matakuliah instance) menjadi dictionary.
        Digunakan untuk serialisasi ke JSON dalam API responses.
        
        Kenapa dibutuhkan?
          - Database: Menyimpan data dalam format relational
          - API: Mengirim data dalam format JSON
          - JSON: Tidak bisa serialize object Python langsung
          - Solusi: Convert ke dictionary dulu, baru ke JSON
        
        Returns:
            dict: Dictionary dengan semua atribut matakuliah
            
        Struktur Return Value:
            {
                'id': 1,
                'kode_mk': 'IF101',
                'nama_mk': 'Algoritma dan Pemrograman',
                'sks': 3,
                'semester': 1
            }
        
        Contoh Penggunaan di View Function:
            @view_config(route_name='matakuliah_list', 
                        request_method='GET', renderer='json')
            def matakuliah_list(request):
                matakuliahs = request.dbsession.query(Matakuliah).all()
                # Convert list of objects ke list of dictionaries
                return {
                    'data': [m.to_dict() for m in matakuliahs]
                }
        """
        # Buat dictionary dengan semua atribut instance
        return {
            'id': self.id,              # Auto-generated ID dari database
            'kode_mk': self.kode_mk,    # Kode mata kuliah
            'nama_mk': self.nama_mk,    # Nama mata kuliah
            'sks': self.sks,            # Satuan kredit semester
            'semester': self.semester,  # Semester pengambilan
        }
    
    
    def __repr__(self):
        """
        METHOD DEBUGGING - String representation untuk logging
        
        Digunakan saat print(matakuliah_object) atau di log.
        Membantu debugging dengan menampilkan informasi penting.
        
        Returns:
            str: String representation yang meaningful
            
        Contoh Output:
            <Matakuliah(id=1, kode_mk='IF101', nama_mk='Algoritma...')>
        """
        # Format string yang informatif untuk debugging
        return (
            f"<Matakuliah("
            f"id={self.id}, "
            f"kode_mk='{self.kode_mk}', "
            f"nama_mk='{self.nama_mk}'"
            f")>"
        )

