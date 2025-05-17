import os
import tempfile
from models import Book
from storage import load_books, save_books

def test_save_and_load_books():
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Prepare test data
        books = [
            Book(ISBN="9780132350884", Title="Clean Code", Author="Robert C. Martin", CopiesTotal=3, CopiesAvailable=3),
            Book(ISBN="9781491957660", Title="Fluent Python", Author="Luciano Ramalho", CopiesTotal=2, CopiesAvailable=1),
        ]

        # Save books to CSV in tmpdir
        save_books("data/", books)

        # # Load books back
        loaded_books = load_books("data/")

        # # # Assert the loaded books match the saved books
        assert len(loaded_books) == len(books)
        print(len(loaded_books) == len(books))
        for original, loaded in zip(books, loaded_books):
            assert original.ISBN == loaded.ISBN
            assert original.Title == loaded.Title
            assert original.Author == loaded.Author
            assert original.CopiesTotal == loaded.CopiesTotal
            assert original.CopiesAvailable == loaded.CopiesAvailable

test_save_and_load_books()