"""
book.py
Class Book sebagai turunan dari LibraryItem

Author: Martino Kelvin_123140165
"""

from library_item import LibraryItem


class Book(LibraryItem):
    """
    Class Book
    Menerapkan inheritance dari LibraryItem
    dan polymorphism untuk display_info()
    """

    def __init__(self, item_id: str, title: str, year: int,
                 author: str, isbn: str, pages: int):
        super().__init__(item_id, title, year)
        self.author = author
        self.isbn = isbn
        self.pages = pages

    def get_category(self) -> str:
        """Mengembalikan kategori item"""
        return "Buku"

    def display_info(self) -> str:
        """Menampilkan info detail buku"""
        status = "Tersedia" if self.is_available else "Dipinjam"
        info = (
            f"[BUKU] {self.title}\n"
            f" - ID       : {self.item_id}\n"
            f" - Tahun    : {self.year}\n"
            f" - Penulis  : {self.author}\n"
            f" - ISBN     : {self.isbn}\n"
            f" - Halaman  : {self.pages}\n"
            f" - Status   : {status}\n"
        )
        return info

    def __str__(self) -> str:
        return f"Buku: {self.title} ({self.year})"
