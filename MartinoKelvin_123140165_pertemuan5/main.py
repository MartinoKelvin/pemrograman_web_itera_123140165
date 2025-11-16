"""
Sistem Manajemen Perpustakaan Sederhana - Main Program
Implementasi OOP dengan Python

Author: Martino Kelvin_123140165

File Structure:
- main.py (this file): Entry point program
- library_item.py: Abstract base class
- book.py: Book class
- magazine.py: Magazine class  
- library.py: Library management class
"""

from book import Book
from magazine import Magazine
from library import Library


def print_header():
    """Menampilkan header program"""
    print("\n" + "="*60)
    print("  SISTEM MANAJEMEN PERPUSTAKAAN SEDERHANA")
    print("  Implementasi OOP dengan Python")
    print("="*60 + "\n")


def print_section(title: str):
    """Menampilkan section header"""
    print("\n" + "="*60)
    print(f"  {title.upper()}")
    print("="*60)


def demo_add_items(library: Library):
    """Demo menambahkan item ke perpustakaan"""
    print_section("Menambahkan Item ke Perpustakaan")
    
    # Menambahkan buku
    books = [
        Book("B001", "Pemrograman Python", 2024, 
             "John Doe", "978-1234567890", 350),
        Book("B002", "Machine Learning Fundamentals", 2023,
             "Jane Smith", "978-0987654321", 450),
        Book("B003", "Data Science dengan Python", 2024,
             "Ahmad Ibrahim", "978-1122334455", 400)
    ]
    
    # Menambahkan majalah
    magazines = [
        Magazine("M001", "Tech Monthly", 2024,
                "Tech Publisher", 145, "November"),
        Magazine("M002", "Science Today", 2024,
                "Science Press", 89, "Oktober")
    ]
    
    for book in books:
        library.add_item(book)
    
    for magazine in magazines:
        library.add_item(magazine)


def demo_display_items(library: Library):
    """Demo menampilkan semua item"""
    print_section("Daftar Semua Item")
    library.display_all_items()


def demo_item_details(library: Library):
    """Demo menampilkan detail item"""
    print_section("Detail Item")
    
    book = library.search_by_id("B001")
    if book:
        print(book.display_info())
    
    magazine = library.search_by_id("M001")
    if magazine:
        print(magazine.display_info())


def demo_search(library: Library):
    """Demo pencarian item"""
    print_section("Pencarian Berdasarkan Judul: 'Python'")
    
    results = library.search_by_title("Python")
    if results:
        for item in results:
            print(f"✓ Ditemukan: {item}")
    else:
        print("❌ Tidak ada hasil")


def demo_borrowing(library: Library):
    """Demo peminjaman item"""
    print_section("Simulasi Peminjaman")
    
    library.borrow_item("B001")
    library.borrow_item("M001")
    
    print_section("Daftar Setelah Peminjaman")
    library.display_all_items()
    
    print_section("Simulasi Pengembalian")
    library.return_item("B001")


def demo_statistics(library: Library):
    """Demo statistik perpustakaan"""
    library.get_statistics()


def main():
    """Fungsi utama untuk menjalankan program"""
    
    # Membuat instance Library
    library = Library("Perpustakaan ITERA")
    
    # Menampilkan header
    print_header()
    
    # Demo berbagai fitur
    demo_add_items(library)
    demo_display_items(library)
    demo_item_details(library)
    demo_search(library)
    demo_borrowing(library)
    demo_statistics(library)


if __name__ == "__main__":
    main()