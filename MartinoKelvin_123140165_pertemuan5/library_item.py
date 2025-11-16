"""
library_item.py
Abstract Base Class untuk semua item di perpustakaan

Author: Martino Kelvin_123140165
"""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """
    Abstract Base Class untuk semua item di perpustakaan.
    Menerapkan konsep Abstraction dan Encapsulation.
    """
    
    def __init__(self, item_id: str, title: str, year: int):
        """
        Constructor untuk LibraryItem
        
        Args:
            item_id: ID unik item
            title: Judul item
            year: Tahun publikasi
        """
        self.__item_id = item_id  # Private attribute
        self._title = title  # Protected attribute
        self._year = year
        self._is_available = True
    
    # Property decorator untuk encapsulation
    @property
    def item_id(self) -> str:
        """Getter untuk item_id"""
        return self.__item_id
    
    @property
    def title(self) -> str:
        """Getter untuk title"""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """
        Setter untuk title dengan validasi
        
        Args:
            value: Judul baru
            
        Raises:
            ValueError: Jika judul kosong
        """
        if not value or len(value.strip()) == 0:
            raise ValueError("Judul tidak boleh kosong")
        self._title = value
    
    @property
    def year(self) -> int:
        """Getter untuk year"""
        return self._year
    
    @property
    def is_available(self) -> bool:
        """Getter untuk status ketersediaan"""
        return self._is_available
    
    def borrow(self) -> bool:
        """
        Method untuk meminjam item
        
        Returns:
            True jika berhasil, False jika item tidak tersedia
        """
        if self._is_available:
            self._is_available = False
            return True
        return False
    
    def return_item(self) -> bool:
        """
        Method untuk mengembalikan item
        
        Returns:
            True jika berhasil, False jika item sudah tersedia
        """
        if not self._is_available:
            self._is_available = True
            return True
        return False
    
    @abstractmethod
    def display_info(self) -> str:
        """
        Abstract method yang harus diimplementasikan oleh subclass
        untuk menampilkan informasi item
        
        Returns:
            String berisi informasi lengkap item
        """
        pass
    
    @abstractmethod
    def get_category(self) -> str:
        """
        Abstract method untuk mendapatkan kategori item
        
        Returns:
            String kategori item
        """
        pass
    
    def __str__(self) -> str:
        """String representation untuk debugging"""
        status = "Tersedia" if self._is_available else "Dipinjam"
        return f"{self.get_category()} - {self._title} ({status})"