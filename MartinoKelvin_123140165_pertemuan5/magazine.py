"""
magazine.py
Class Magazine sebagai turunan dari LibraryItem

Author: Martino Kelvin_123140165
"""

from library_item import LibraryItem


class Magazine(LibraryItem):
    """
    Class Magazine
    Menerapkan inheritance dari LibraryItem
    dan polymorphism untuk display_info()
    """

    def __init__(self, item_id: str, title: str, year: int,
                 publisher: str, issue_number: int, month: str):
        super().__init__(item_id, title, year)
        self.publisher = publisher
        self.issue_number = issue_number
        self.month = month

    def get_category(self) -> str:
        """Kategori item"""
        return "Majalah"

    def display_info(self) -> str:
        """Menampilkan info majalah"""
        status = "Tersedia" if self.is_available else "Dipinjam"
        info = (
            f"[MAJALAH] {self.title}\n"
            f" - ID         : {self.item_id}\n"
            f" - Tahun      : {self.year}\n"
            f" - Penerbit   : {self.publisher}\n"
            f" - Edisi      : {self.issue_number} ({self.month})\n"
            f" - Status     : {status}\n"
        )
        return info

    def __str__(self) -> str:
        return f"Majalah: {self.title} ({self.month} {self.year})"
