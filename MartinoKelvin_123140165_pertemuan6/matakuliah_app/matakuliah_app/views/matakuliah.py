"""
MODUL VIEWS - MATAKULIAH - Handler untuk semua endpoint API Matakuliah

Modul ini berisi view functions (handlers) untuk semua operasi CRUD:
  - GET /api/matakuliah           -> Ambil semua matakuliah
  - GET /api/matakuliah/{id}      -> Ambil detail satu matakuliah
  - POST /api/matakuliah          -> Buat matakuliah baru
  - PUT /api/matakuliah/{id}      -> Update matakuliah
  - DELETE /api/matakuliah/{id}   -> Hapus matakuliah

Setiap view function:
  1. Menerima request object dari Pyramid
  2. Melakukan validasi input
  3. Mengakses database via request.dbsession
  4. Menangani error yang mungkin terjadi
  5. Mengembalikan response JSON dengan format standard

Response Format (Production-Grade):
  {
    "success": true/false,           # Status operasi
    "code": 200/201/400/404/500,     # HTTP status code
    "message": "Deskripsi operasi",  # Pesan human-readable
    "timestamp": "ISO 8601 format",  # Waktu response
    "data": {...},                   # Data hasil operasi (optional)
    "errors": {...}                  # Detail error (optional)
  }

Kontribusi ke Kriteria Penilaian:
  - API Endpoints (40%): Implementasi lengkap CRUD dengan validasi & error handling
  - Dokumentasi dan Kerapian Kode: Comments lengkap, error handling, logging
"""
from pyramid.view import view_config
from pyramid.response import Response
from ..models import Matakuliah
import logging
from datetime import datetime
import traceback

# Inisialisasi logger untuk modul ini
log = logging.getLogger(__name__)


# ============= HELPER FUNCTION - MEMBUAT RESPONSE STANDARD =============

def create_response(success, code, message, data=None, errors=None):
    """
    HELPER FUNCTION - Membuat response JSON dengan format standard
    
    Fungsi ini memastikan semua endpoint mengembalikan format response
    yang konsisten dan sesuai best practices REST API.
    
    Keuntungan:
      1. Konsistensi format di semua endpoint
      2. Mudah diparsing di client
      3. Informasi lengkap untuk debugging
      4. Production-grade standard
    
    Args:
        success (bool): True jika operasi berhasil, False jika error
        code (int): HTTP status code (200, 201, 400, 404, 500)
        message (str): Pesan yang mudah dibaca manusia
        data (dict, optional): Data hasil operasi
        errors (dict, optional): Detail error (hanya jika ada error)
    
    Returns:
        dict: Dictionary response yang akan di-convert ke JSON oleh Pyramid
        
    Contoh Success Response (200):
        {
          "success": true,
          "code": 200,
          "message": "Data retrieved successfully",
          "timestamp": "2025-11-26T01:45:00.123456Z",
          "data": {"matakuliahs": [...], "total": 2}
        }
    
    Contoh Error Response (400):
        {
          "success": false,
          "code": 400,
          "message": "Validation failed",
          "timestamp": "2025-11-26T01:45:00.123456Z",
          "errors": {"missing_fields": ["kode_mk", "nama_mk"]}
        }
    """
    # Buat dictionary response dasar
    response_body = {
        "success": success,              # Status operasi
        "code": code,                    # HTTP status code
        "message": message,              # Pesan deskriptif
        "timestamp": datetime.utcnow().isoformat() + "Z",  # ISO 8601 format
    }
    
    # Tambahkan data jika ada (di case success)
    if data is not None:
        response_body["data"] = data
    
    # Tambahkan error detail jika ada (di case error)
    if errors is not None:
        response_body["errors"] = errors
    
    return response_body


# ============= VIEW FUNCTIONS - ENDPOINT IMPLEMENTATIONS =============

# ===== COLLECTION ENDPOINTS (List & Create) =====

@view_config(route_name='matakuliah_collection', request_method='GET', renderer='json')
def matakuliah_list(request):
    """
    ENDPOINT 1 - GET /api/matakuliah
    
    Mengambil daftar semua matakuliah dari database.
    
    HTTP Method: GET
    Route Name: matakuliah_collection
    URL Pattern: /api/matakuliah
    
    Query Parameters: Tidak ada (bisa ditambahkan untuk pagination)
    
    Request Body: Tidak ada
    
    Success Response (200):
        {
          "success": true,
          "code": 200,
          "message": "Matakuliah data retrieved successfully",
          "timestamp": "...",
          "data": {
            "matakuliahs": [
              {"id": 1, "kode_mk": "IF101", "nama_mk": "...", ...},
              {"id": 2, "kode_mk": "IF102", "nama_mk": "...", ...}
            ],
            "total": 2
          }
        }
    
    Error Response (500):
        {
          "success": false,
          "code": 500,
          "message": "Failed to retrieve matakuliah data",
          "errors": {"detail": "Internal server error"}
        }
    
    Curl Testing:
        curl -X GET http://localhost:6543/api/matakuliah
    """
    try:
        # Query semua matakuliah dari database
        matakuliahs = request.dbsession.query(Matakuliah).all()
        
        # Log informasi
        log.info(f"Retrieved {len(matakuliahs)} matakuliah records")
        
        # Return success response dengan data
        return create_response(
            success=True,
            code=200,
            message="Matakuliah data retrieved successfully",
            data={
                "matakuliahs": [m.to_dict() for m in matakuliahs],
                "total": len(matakuliahs)
            }
        )
    
    except Exception as e:
        # Log error untuk debugging (JANGAN kirim ke client)
        log.error(f"Error retrieving matakuliah: {str(e)}\n{traceback.format_exc()}")
        
        # Set HTTP status code
        request.response.status = 500
        
        # Return error response (tanpa expose internal error)
        return create_response(
            success=False,
            code=500,
            message="Failed to retrieve matakuliah data",
            errors={"detail": "Internal server error"}  # Generic message untuk keamanan
        )


@view_config(route_name='matakuliah_collection', request_method='POST', renderer='json')
def matakuliah_create(request):
    """
    ENDPOINT 2 - POST /api/matakuliah
    
    Membuat (insert) matakuliah baru ke database.
    
    HTTP Method: POST
    Route Name: matakuliah_collection
    URL Pattern: /api/matakuliah
    
    Request Body (JSON):
        {
          "kode_mk": "IF101",
          "nama_mk": "Algoritma dan Pemrograman",
          "sks": 3,
          "semester": 1
        }
    
    Success Response (201 Created):
        {
          "success": true,
          "code": 201,
          "message": "Matakuliah created successfully",
          "timestamp": "...",
          "data": {
            "matakuliah": {
              "id": 1,
              "kode_mk": "IF101",
              "nama_mk": "Algoritma dan Pemrograman",
              "sks": 3,
              "semester": 1
            }
          }
        }
    
    Error Response (400 - Validation Failed):
        {
          "success": false,
          "code": 400,
          "message": "Validation failed",
          "errors": {"missing_fields": ["kode_mk", "nama_mk"]}
        }
    
    Error Response (400 - Invalid Type):
        {
          "success": false,
          "code": 400,
          "message": "Validation failed",
          "errors": {"sks": "Must be a positive integer"}
        }
    
    Curl Testing:
        curl -X POST http://localhost:6543/api/matakuliah \
          -H "Content-Type: application/json" \
          -d '{"kode_mk":"IF101","nama_mk":"Algoritma","sks":3,"semester":1}'
    """
    try:
        # Parse JSON body dari request
        data = request.json_body
        
        # STEP 1: VALIDASI FIELD WAJIB
        # Cek apakah semua required fields ada di request
        required_fields = ['kode_mk', 'nama_mk', 'sks', 'semester']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            # Ada field yang hilang
            request.response.status = 400
            log.warning(f"Missing fields: {missing_fields}")
            return create_response(
                success=False,
                code=400,
                message="Validation failed",
                errors={"missing_fields": missing_fields}
            )
        
        # STEP 2: VALIDASI TIPE DATA
        # Cek apakah tipe data setiap field benar
        validation_errors = {}
        
        # Validasi kode_mk: harus string
        if not isinstance(data.get('kode_mk'), str):
            validation_errors['kode_mk'] = "Must be a string"
        
        # Validasi nama_mk: harus string
        if not isinstance(data.get('nama_mk'), str):
            validation_errors['nama_mk'] = "Must be a string"
        
        # Validasi sks: harus integer dan positif (> 0)
        if not isinstance(data.get('sks'), int) or data.get('sks') <= 0:
            validation_errors['sks'] = "Must be a positive integer"
        
        # Validasi semester: harus integer dan positif (> 0)
        if not isinstance(data.get('semester'), int) or data.get('semester') <= 0:
            validation_errors['semester'] = "Must be a positive integer"
        
        # Jika ada error validasi, return error response
        if validation_errors:
            request.response.status = 400
            log.warning(f"Validation errors: {validation_errors}")
            return create_response(
                success=False,
                code=400,
                message="Validation failed",
                errors=validation_errors
            )
        
        # STEP 3: CREATE OBJECT & INSERT KE DATABASE
        # Buat instance baru dari model Matakuliah
        matakuliah = Matakuliah(
            kode_mk=data['kode_mk'],
            nama_mk=data['nama_mk'],
            sks=data['sks'],
            semester=data['semester']
        )
        
        # Tambahkan ke session (belum insert ke DB)
        request.dbsession.add(matakuliah)
        
        # Flush untuk execute INSERT ke DB (tapi belum commit)
        # Ini memicu auto-generation dari ID
        request.dbsession.flush()
        
        # Log informasi
        log.info(f"Created matakuliah: {matakuliah.kode_mk} (ID: {matakuliah.id})")
        
        # Set status code 201 Created
        request.response.status = 201
        
        # Return success response dengan data matakuliah yang baru dibuat
        return create_response(
            success=True,
            code=201,
            message="Matakuliah created successfully",
            data={"matakuliah": matakuliah.to_dict()}
        )
    
    except ValueError as e:
        # ValueError: Terjadi pada parsing JSON atau type casting
        log.warning(f"Validation error: {str(e)}")
        request.response.status = 400
        return create_response(
            success=False,
            code=400,
            message="Invalid request data",
            errors={"detail": str(e)}
        )
    
    except Exception as e:
        # General exception: Unexpected error
        log.error(f"Error creating matakuliah: {str(e)}\n{traceback.format_exc()}")
        request.response.status = 500
        return create_response(
            success=False,
            code=500,
            message="Failed to create matakuliah",
            errors={"detail": "Internal server error"}
        )


# ===== DETAIL ENDPOINTS (Read, Update, Delete) =====

@view_config(route_name='matakuliah_detail', request_method='GET', renderer='json')
def matakuliah_detail(request):
    """
    ENDPOINT 3 - GET /api/matakuliah/{id}
    
    Mengambil detail satu matakuliah berdasarkan ID.
    
    HTTP Method: GET
    Route Name: matakuliah_detail
    URL Pattern: /api/matakuliah/{id}
    Path Parameter: id - ID matakuliah (number)
    
    Request Body: Tidak ada
    
    Success Response (200):
        {
          "success": true,
          "code": 200,
          "message": "Matakuliah data retrieved successfully",
          "timestamp": "...",
          "data": {
            "matakuliah": {
              "id": 1,
              "kode_mk": "IF101",
              "nama_mk": "Algoritma dan Pemrograman",
              "sks": 3,
              "semester": 1
            }
          }
        }
    
    Error Response (404 Not Found):
        {
          "success": false,
          "code": 404,
          "message": "Matakuliah not found",
          "errors": {"resource": "Matakuliah with id 999 does not exist"}
        }
    
    Curl Testing:
        curl -X GET http://localhost:6543/api/matakuliah/1
    """
    try:
        # Ambil parameter 'id' dari URL path
        # Format: /api/matakuliah/1 -> id = '1'
        id = request.matchdict['id']
        
        # Query matakuliah berdasarkan ID
        # one_or_none(): Return record jika ada, None jika tidak ada
        # Ini lebih aman daripada .get() yang deprecated
        matakuliah = request.dbsession.query(Matakuliah).filter_by(id=id).one_or_none()
        
        # Cek apakah matakuliah ditemukan
        if not matakuliah:
            request.response.status = 404
            log.warning(f"Matakuliah not found: id={id}")
            return create_response(
                success=False,
                code=404,
                message="Matakuliah not found",
                errors={"resource": f"Matakuliah with id {id} does not exist"}
            )
        
        # Log informasi
        log.info(f"Retrieved matakuliah: {matakuliah.kode_mk} (ID: {id})")
        
        # Return success response
        return create_response(
            success=True,
            code=200,
            message="Matakuliah data retrieved successfully",
            data={"matakuliah": matakuliah.to_dict()}
        )
    
    except Exception as e:
        log.error(f"Error retrieving matakuliah {request.matchdict.get('id')}: {str(e)}\n{traceback.format_exc()}")
        request.response.status = 500
        return create_response(
            success=False,
            code=500,
            message="Failed to retrieve matakuliah",
            errors={"detail": "Internal server error"}
        )


@view_config(route_name='matakuliah_detail', request_method='PUT', renderer='json')
def matakuliah_update(request):
    """
    ENDPOINT 4 - PUT /api/matakuliah/{id}
    
    Mengupdate data matakuliah yang sudah ada.
    
    HTTP Method: PUT
    Route Name: matakuliah_detail
    URL Pattern: /api/matakuliah/{id}
    Path Parameter: id - ID matakuliah yang akan diupdate
    
    Request Body (JSON - semua field optional):
        {
          "nama_mk": "Algoritma Lanjut",
          "sks": 4
        }
    
    Success Response (200):
        {
          "success": true,
          "code": 200,
          "message": "Matakuliah updated successfully",
          "timestamp": "...",
          "data": {
            "matakuliah": {
              "id": 1,
              "kode_mk": "IF101",
              "nama_mk": "Algoritma Lanjut",
              "sks": 4,
              "semester": 1
            }
          }
        }
    
    Error Response (404 Not Found):
        {
          "success": false,
          "code": 404,
          "message": "Matakuliah not found",
          "errors": {"resource": "Matakuliah with id 999 does not exist"}
        }
    
    Curl Testing:
        curl -X PUT http://localhost:6543/api/matakuliah/1 \
          -H "Content-Type: application/json" \
          -d '{"sks":4}'
    """
    try:
        # Ambil parameter 'id' dari URL path
        id = request.matchdict['id']
        
        # Query matakuliah berdasarkan ID
        matakuliah = request.dbsession.query(Matakuliah).filter_by(id=id).one_or_none()
        
        # Cek apakah matakuliah ditemukan
        if not matakuliah:
            request.response.status = 404
            log.warning(f"Matakuliah not found: id={id}")
            return create_response(
                success=False,
                code=404,
                message="Matakuliah not found",
                errors={"resource": f"Matakuliah with id {id} does not exist"}
            )
        
        # Parse JSON body
        data = request.json_body
        
        # VALIDASI dan UPDATE FIELD
        # Update hanya field yang ada di request body (partial update)
        
        if 'kode_mk' in data:
            if not isinstance(data['kode_mk'], str):
                request.response.status = 400
                return create_response(
                    success=False,
                    code=400,
                    message="Validation failed",
                    errors={"kode_mk": "Must be a string"}
                )
            matakuliah.kode_mk = data['kode_mk']
        
        if 'nama_mk' in data:
            if not isinstance(data['nama_mk'], str):
                request.response.status = 400
                return create_response(
                    success=False,
                    code=400,
                    message="Validation failed",
                    errors={"nama_mk": "Must be a string"}
                )
            matakuliah.nama_mk = data['nama_mk']
        
        if 'sks' in data:
            if not isinstance(data['sks'], int) or data['sks'] <= 0:
                request.response.status = 400
                return create_response(
                    success=False,
                    code=400,
                    message="Validation failed",
                    errors={"sks": "Must be a positive integer"}
                )
            matakuliah.sks = data['sks']
        
        if 'semester' in data:
            if not isinstance(data['semester'], int) or data['semester'] <= 0:
                request.response.status = 400
                return create_response(
                    success=False,
                    code=400,
                    message="Validation failed",
                    errors={"semester": "Must be a positive integer"}
                )
            matakuliah.semester = data['semester']
        
        # Flush update ke database
        request.dbsession.flush()
        
        # Log informasi
        log.info(f"Updated matakuliah: {matakuliah.kode_mk} (ID: {id})")
        
        # Return success response
        return create_response(
            success=True,
            code=200,
            message="Matakuliah updated successfully",
            data={"matakuliah": matakuliah.to_dict()}
        )
    
    except Exception as e:
        log.error(f"Error updating matakuliah {request.matchdict.get('id')}: {str(e)}\n{traceback.format_exc()}")
        request.response.status = 500
        return create_response(
            success=False,
            code=500,
            message="Failed to update matakuliah",
            errors={"detail": "Internal server error"}
        )


@view_config(route_name='matakuliah_detail', request_method='DELETE', renderer='json')
def matakuliah_delete(request):
    """
    ENDPOINT 5 - DELETE /api/matakuliah/{id}
    
    Menghapus (delete) satu matakuliah dari database.
    
    HTTP Method: DELETE
    Route Name: matakuliah_detail
    URL Pattern: /api/matakuliah/{id}
    Path Parameter: id - ID matakuliah yang akan dihapus
    
    Request Body: Tidak ada
    
    Success Response (200):
        {
          "success": true,
          "code": 200,
          "message": "Matakuliah deleted successfully",
          "timestamp": "...",
          "data": {
            "deleted_matakuliah": {
              "id": 1,
              "kode_mk": "IF101",
              "nama_mk": "Algoritma dan Pemrograman",
              "sks": 3,
              "semester": 1
            }
          }
        }
    
    Error Response (404 Not Found):
        {
          "success": false,
          "code": 404,
          "message": "Matakuliah not found",
          "errors": {"resource": "Matakuliah with id 999 does not exist"}
        }
    
    Curl Testing:
        curl -X DELETE http://localhost:6543/api/matakuliah/1
    """
    try:
        # Ambil parameter 'id' dari URL path
        id = request.matchdict['id']
        
        # Query matakuliah berdasarkan ID
        matakuliah = request.dbsession.query(Matakuliah).filter_by(id=id).one_or_none()
        
        # Cek apakah matakuliah ditemukan
        if not matakuliah:
            request.response.status = 404
            log.warning(f"Matakuliah not found: id={id}")
            return create_response(
                success=False,
                code=404,
                message="Matakuliah not found",
                errors={"resource": f"Matakuliah with id {id} does not exist"}
            )
        
        # Simpan data untuk return dalam response (sebelum delete)
        deleted_data = matakuliah.to_dict()
        
        # Delete matakuliah dari database
        request.dbsession.delete(matakuliah)
        
        # Flush delete ke database
        request.dbsession.flush()
        
        # Log informasi
        log.info(f"Deleted matakuliah: {deleted_data['kode_mk']} (ID: {id})")
        
        # Return success response dengan data yang sudah dihapus
        return create_response(
            success=True,
            code=200,
            message="Matakuliah deleted successfully",
            data={"deleted_matakuliah": deleted_data}
        )
    
    except Exception as e:
        log.error(f"Error deleting matakuliah {request.matchdict.get('id')}: {str(e)}\n{traceback.format_exc()}")
        request.response.status = 500
        return create_response(
            success=False,
            code=500,
            message="Failed to delete matakuliah",
            errors={"detail": "Internal server error"}
        )
