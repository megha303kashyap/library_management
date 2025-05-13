import csv
import os
from models import Book, Member, Loan

def _csv_path(data_dir, name):
    return os.path.join(data_dir, name + '.csv')

def load_books(data_dir):
    books = []
    path = _csv_path(data_dir, 'books')
    if not os.path.exists(path):
        return books
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(Book(**row, CopiesTotal=int(row['CopiesTotal']), CopiesAvailable=int(row['CopiesAvailable'])))
    return books

def save_books(data_dir, books):
    path = _csv_path(data_dir, 'books')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Book.__annotations__.keys())
        writer.writeheader()
        for b in books:
            writer.writerow(b.__dict__)

def load_members(data_dir):
    members = []
    path = _csv_path(data_dir, 'members')
    if not os.path.exists(path):
        return members
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members.append(Member(**row))
    return members

def save_members(data_dir, members):
    path = _csv_path(data_dir, 'members')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Member.__annotations__.keys())
        writer.writeheader()
        for m in members:
            writer.writerow(m.__dict__)

def load_loans(data_dir):
    loans = []
    path = _csv_path(data_dir, 'loans')
    if not os.path.exists(path):
        return loans
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            loans.append(Loan(**row))
    return loans

def save_loans(data_dir, loans):
    path = _csv_path(data_dir, 'loans')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Loan.__annotations__.keys())
        writer.writeheader()
        for l in loans:
            writer.writerow(l.__dict__)
