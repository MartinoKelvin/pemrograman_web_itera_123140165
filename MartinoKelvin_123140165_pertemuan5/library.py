"""
library.py
Class Library untuk manajemen item perpustakaan

Author: Martino Kelvin_123140165
"""

from typing import List, Optional
from library_item import LibraryItem


class Library:
    """
    Class untuk manajemen item perpustakaan.
    Menerapkan encapsulation dan fitur CRUD sederhana.
    """

    def __init__(self, name: str):
        self.name = name
        self.__items: List[LibraryItem] = []  # private list

    # --------------------------
    # Encapsulation via property
    # --------------------------
    @property
    def total_items(self) -> int:
        return len(self.__items)

    @property
    def available_items(self) -> int:
        return len([item for item in self.__items if item.is_available])

    # --------------------------
    # CRUD
    # --------------------------

    def add_item(self, item: LibraryItem) -> bool:
        """
        Menambahkan item ke perpustakaan.
        Tidak boleh ID duplikat.
        """
        if self.search_by_id(item.item_id):
            print(f"❌ Item dengan ID {item.item_id} sudah ada.")
            return False

        self.__items.append(item)
        print(f"✓ Item '{item.title}' berhasil ditambahkan.")
        return True

    def display_all_items(self):
        """Menampilkan seluruh item di perpustakaan."""
        if not self.__items:
            print("Tidak ada item dalam perpustakaan.\n")
            return

        print(f"\n=== DAFTAR ITEM {self.name} ===")
        for item in self.__items:
            print(item.display_info())

    # --------------------------
    # Pencarian
    # --------------------------
    def search_by_id(self, item_id: str) -> Optional[LibraryItem]:
        for item in self.__items:
            if item.item_id == item_id:
                return item
        return None

    def search_by_title(self, title: str) -> List[LibraryItem]:
        return [
            item for item in self.__items
            if title.lower() in item.title.lower()
        ]

    # --------------------------
    # Borrow / Return
    # --------------------------
    def borrow_item(self, item_id: str) -> bool:
        item = self.search_by_id(item_id)
        if not item:
            print(f"❌ Item dengan ID {item_id} tidak ditemukan.")
            return False

        if item.borrow():
            print(f"✓ Item '{item.title}' berhasil dipinjam.")
            return True

        print(f"❌ Item '{item.title}' sedang dipinjam.")
        return False

    def return_item(self, item_id: str) -> bool:
        item = self.search_by_id(item_id)
        if not item:
            print(f"❌ Item dengan ID {item_id} tidak ditemukan.")
            return False

        if item.return_item():
            print(f"✓ Item '{item.title}' berhasil dikembalikan.")
            return True

        print(f"❌ Item '{item.title}' sudah tersedia.")
        return False

    # --------------------------
    # Statistik
    # --------------------------
    def get_statistics(self):
        print("\n=== STATISTIK PERPUSTAKAAN ===")
        print(f"Total Item      : {self.total_items}")
        print(f"Item Tersedia   : {self.available_items}")
        print(f"Item Dipinjam   : {self.total_items - self.available_items}")
        print("==============================\n")
