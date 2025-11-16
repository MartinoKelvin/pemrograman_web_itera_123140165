"""
test_library.py (Optional)
Unit test untuk memvalidasi fungsi-fungsi sistem perpustakaan

Author: Martino Kelvin_123140165

Note: File ini opsional, untuk bonus point jika ingin menambahkan testing
"""

import unittest
from book import Book
from magazine import Magazine
from library import Library


class TestLibraryItem(unittest.TestCase):
    """Test case untuk LibraryItem (Book dan Magazine)"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.book = Book("B001", "Test Book", 2024, "Author", "123", 100)
        self.magazine = Magazine("M001", "Test Mag", 2024, "Pub", 1, "Jan")
    
    def test_book_creation(self):
        """Test pembuatan objek Book"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Author")
        self.assertTrue(self.book.is_available)
    
    def test_magazine_creation(self):
        """Test pembuatan objek Magazine"""
        self.assertEqual(self.magazine.title, "Test Mag")
        self.assertEqual(self.magazine.publisher, "Pub")
        self.assertTrue(self.magazine.is_available)
    
    def test_borrow_item(self):
        """Test peminjaman item"""
        result = self.book.borrow()
        self.assertTrue(result)
        self.assertFalse(self.book.is_available)
        
        # Test borrow item yang sudah dipinjam
        result = self.book.borrow()
        self.assertFalse(result)
    
    def test_return_item(self):
        """Test pengembalian item"""
        self.book.borrow()
        result = self.book.return_item()
        self.assertTrue(result)
        self.assertTrue(self.book.is_available)
        
        # Test return item yang tidak dipinjam
        result = self.book.return_item()
        self.assertFalse(result)
    
    def test_polymorphism(self):
        """Test polymorphism - method yang sama tapi hasil berbeda"""
        book_info = self.book.display_info()
        mag_info = self.magazine.display_info()
        
        self.assertIn("BUKU", book_info.upper())
        self.assertIn("MAJALAH", mag_info.upper())
        self.assertNotEqual(book_info, mag_info)
    
    def test_category(self):
        """Test method get_category"""
        self.assertEqual(self.book.get_category(), "Buku")
        self.assertEqual(self.magazine.get_category(), "Majalah")


class TestLibrary(unittest.TestCase):
    """Test case untuk Library management"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.library = Library("Test Library")
        self.book1 = Book("B001", "Python", 2024, "John", "111", 100)
        self.book2 = Book("B002", "Java", 2024, "Jane", "222", 200)
        self.mag1 = Magazine("M001", "Tech", 2024, "TechPub", 1, "Jan")
    
    def test_add_item(self):
        """Test menambahkan item"""
        result = self.library.add_item(self.book1)
        self.assertTrue(result)
        self.assertEqual(self.library.total_items, 1)
        
        # Test menambahkan item dengan ID yang sama
        duplicate = Book("B001", "Duplicate", 2024, "X", "333", 50)
        result = self.library.add_item(duplicate)
        self.assertFalse(result)
        self.assertEqual(self.library.total_items, 1)
    
    def test_search_by_id(self):
        """Test pencarian berdasarkan ID"""
        self.library.add_item(self.book1)
        
        result = self.library.search_by_id("B001")
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Python")
        
        result = self.library.search_by_id("XXX")
        self.assertIsNone(result)
    
    def test_search_by_title(self):
        """Test pencarian berdasarkan judul"""
        self.library.add_item(self.book1)
        self.library.add_item(self.book2)
        
        results = self.library.search_by_title("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python")
        
        results = self.library.search_by_title("xyz")
        self.assertEqual(len(results), 0)
    
    def test_borrow_item(self):
        """Test peminjaman item dari library"""
        self.library.add_item(self.book1)
        
        result = self.library.borrow_item("B001")
        self.assertTrue(result)
        self.assertEqual(self.library.available_items, 0)
        
        # Test borrow item yang tidak ada
        result = self.library.borrow_item("XXX")
        self.assertFalse(result)
    
    def test_return_item(self):
        """Test pengembalian item ke library"""
        self.library.add_item(self.book1)
        self.library.borrow_item("B001")
        
        result = self.library.return_item("B001")
        self.assertTrue(result)
        self.assertEqual(self.library.available_items, 1)
    
    def test_statistics(self):
        """Test perhitungan statistik"""
        self.library.add_item(self.book1)
        self.library.add_item(self.book2)
        self.library.add_item(self.mag1)
        
        self.assertEqual(self.library.total_items, 3)
        self.assertEqual(self.library.available_items, 3)
        
        self.library.borrow_item("B001")
        self.assertEqual(self.library.available_items, 2)
    
    def test_property_decorator(self):
        """Test property decorator dengan setter"""
        try:
            self.book1.title = "New Title"
            self.assertEqual(self.book1.title, "New Title")
        except Exception as e:
            self.fail(f"Setting valid title should not raise exception: {e}")
        
        # Test setter dengan validasi
        with self.assertRaises(ValueError):
            self.book1.title = ""
        
        with self.assertRaises(ValueError):
            self.book1.title = "   "


class TestEncapsulation(unittest.TestCase):
    """Test case untuk encapsulation"""
    
    def test_private_attributes(self):
        """Test bahwa private attributes tidak bisa diakses langsung"""
        book = Book("B001", "Test", 2024, "Author", "123", 100)
        
        # Private attribute tidak bisa diakses langsung
        with self.assertRaises(AttributeError):
            _ = book.__item_id
        
        # Tapi bisa diakses lewat property
        self.assertEqual(book.item_id, "B001")
    
    def test_protected_attributes(self):
        """Test protected attributes"""
        book = Book("B001", "Test", 2024, "Author", "123", 100)
        
        # Protected attribute bisa diakses (tapi tidak disarankan)
        self.assertEqual(book._title, "Test")


def run_tests():
    """Menjalankan semua test"""
    print("\n" + "="*60)
    print("  RUNNING UNIT TESTS")
    print("="*60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestLibraryItem))
    suite.addTests(loader.loadTestsFromTestCase(TestLibrary))
    suite.addTests(loader.loadTestsFromTestCase(TestEncapsulation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)