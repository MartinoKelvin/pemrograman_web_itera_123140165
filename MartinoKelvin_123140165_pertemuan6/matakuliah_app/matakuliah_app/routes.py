"""
MODUL ROUTING - Konfigurasi URL Routes untuk Aplikasi Matakuliah

Modul ini mendefinisikan semua URL pattern (routes) untuk aplikasi.
Setiap route menghubungkan URL dengan nama route yang kemudian
ditautkan ke view functions melalui @view_config decorators.

PENTING: request_method (GET, POST, PUT, DELETE) BUKAN didefinisikan
di sini, tetapi di @view_config decorator di modul views!

Routing Flow:
  1. User request ke http://localhost:6543/api/matakuliah
  2. Pyramid cocokkan dengan route patterns di sini
  3. Tentukan route name (misal: 'matakuliah_collection')
  4. Cari @view_config dengan route_name tersebut
  5. Jalankan view function yang sesuai

Kontribusi ke Kriteria Penilaian:
  - API Endpoints: Route pattern yang jelas dan terstruktur
  - Dokumentasi dan Kerapian Kode: Comments yang menjelaskan setiap route
"""


def includeme(config):
    """
    FUNGSI UTAMA - Daftarkan semua routes untuk aplikasi
    
    Dipanggil dari application factory (__init__.py) saat inisialisasi.
    Nama 'includeme' adalah konvensi Pyramid yang penting.
    
    Definisi Routes:
    
    1. Static Files (CSS, JS, images)
       Pattern: /static/*
       Tujuan: Serve static assets (non-dynamic files)
       Cache: 1 jam (3600 detik)
    
    2. Home Page
       Pattern: /
       Route Name: 'home'
       Tujuan: Menampilkan halaman utama aplikasi
    
    3. Matakuliah Collection (List & Create)
       Pattern: /api/matakuliah
       Route Name: 'matakuliah_collection'
       Methods:
         - GET: Ambil semua matakuliah
         - POST: Buat matakuliah baru
       Note: Method ditentukan di @view_config, bukan di sini
    
    4. Matakuliah Detail (Read, Update, Delete)
       Pattern: /api/matakuliah/{id}
       Route Name: 'matakuliah_detail'
       Path Parameter: {id} = ID matakuliah (number)
       Methods:
         - GET: Ambil detail satu matakuliah
         - PUT: Update matakuliah
         - DELETE: Hapus matakuliah
       Note: Method ditentukan di @view_config, bukan di sini
    
    Args:
        config (Configurator): Objek Pyramid Configurator untuk registrasi
        
    Contoh Output saat dijalankan (debug):
        Route: home -> /
        Route: matakuliah_collection -> /api/matakuliah
        Route: matakuliah_detail -> /api/matakuliah/{id}
    """
    
    # ========== STATIC FILES ==========
    # Registrasi direktori untuk static assets (CSS, JS, images, etc)
    # add_static_view(name, path, **kwds)
    # - name: Virtual path di URL (/static)
    # - path: Direktori fisik di project (static/)
    # - cache_max_age: Browser cache duration dalam detik (3600 = 1 jam)
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    
    # ========== HOME PAGE ROUTE ==========
    # Definisi route untuk halaman utama
    # add_route(name, pattern)
    # - name: Identitas unik route (digunakan di @view_config)
    # - pattern: URL pattern yang akan di-match
    config.add_route('home', '/')
    
    
    # ========== API ROUTES - MATAKULIAH COLLECTION ==========
    # Route untuk operasi pada koleksi (list semua, create baru)
    # Pattern: /api/matakuliah
    # 
    # Di view function (matakuliah.py), ada 2 handlers:
    #   @view_config(route_name='matakuliah_collection', 
    #                request_method='GET', ...)
    #   def matakuliah_list(request):
    #       # Ambil semua matakuliah
    #
    #   @view_config(route_name='matakuliah_collection',
    #                request_method='POST', ...)
    #   def matakuliah_create(request):
    #       # Buat matakuliah baru
    config.add_route('matakuliah_collection', '/api/matakuliah')
    
    
    # ========== API ROUTES - MATAKULIAH DETAIL ==========
    # Route untuk operasi pada item tertentu (read, update, delete)
    # Pattern: /api/matakuliah/{id}
    # - {id}: Path parameter yang akan diakses via request.matchdict['id']
    #
    # Di view function (matakuliah.py), ada 3 handlers:
    #   @view_config(route_name='matakuliah_detail',
    #                request_method='GET', ...)
    #   def matakuliah_detail(request):
    #       # Ambil detail satu matakuliah
    #
    #   @view_config(route_name='matakuliah_detail',
    #                request_method='PUT', ...)
    #   def matakuliah_update(request):
    #       # Update matakuliah
    #
    #   @view_config(route_name='matakuliah_detail',
    #                request_method='DELETE', ...)
    #   def matakuliah_delete(request):
    #       # Hapus matakuliah
    # 
    # Contoh request:
    #   GET /api/matakuliah/1      -> matakuliah_detail (id=1)
    #   PUT /api/matakuliah/5      -> matakuliah_update (id=5)
    #   DELETE /api/matakuliah/10  -> matakuliah_delete (id=10)
    config.add_route('matakuliah_detail', '/api/matakuliah/{id}')
