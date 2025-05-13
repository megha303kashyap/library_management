import argparse
import os
from datetime import datetime, timedelta
from models import Book, Member, Loan
from storage import (
    load_books, save_books,
    load_members, save_members,
    load_loans, save_loans
)
from auth import register_member, login

def valid_isbn(isbn):
    return isbn.isdigit() and (len(isbn) == 10 or len(isbn) == 13)

def next_loan_id(loans):
    return str(max([int(l.LoanID) for l in loans], default=1000) + 1)

def librarian_menu(data_dir, session):
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book\n2. Register Member\n3. Issue Book\n4. Return Book\n5. Overdue List\n6. Logout")
        choice = input("> ").strip()
        if choice == '1':
            add_book(data_dir)
        elif choice == '2':
            register_member_flow(data_dir)
        elif choice == '3':
            issue_book(data_dir)
        elif choice == '4':
            return_book(data_dir)
        elif choice == '5':
            overdue_list(data_dir)
        elif choice == '6':
            break

def member_menu(data_dir, session):
    while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Catalogue\n2. Borrow Book\n3. My Loans\n4. Logout")
        choice = input("> ").strip()
        if choice == '1':
            search_catalogue(data_dir)
        elif choice == '2':
            borrow_book(data_dir, session['user'])
        elif choice == '3':
            my_loans(data_dir, session['user'])
        elif choice == '4':
            break

def add_book(data_dir):
    isbn = input("ISBN: ").strip()
    if not valid_isbn(isbn):
        print("Invalid ISBN.")
        return
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    try:
        copies = int(input("Total Copies: ").strip())
        if copies < 1:
            raise ValueError
    except ValueError:
        print("Invalid number of copies.")
        return
    books = load_books(data_dir)
    if any(b.ISBN == isbn for b in books):
        print("Book already exists.")
        return
    book = Book(ISBN=isbn, Title=title, Author=author, CopiesTotal=copies, CopiesAvailable=copies)
    books.append(book)
    save_books(data_dir, books)
    print("✔ Book added.")

def register_member_flow(data_dir):
    name = input("Name: ").strip()
    member_id = input("Member ID: ").strip()
    pw1 = input("Password: ").strip()
    pw2 = input("Confirm Password: ").strip()
    if pw1 != pw2:
        print("Password mismatch.")
        return
    try:
        register_member(data_dir, name, member_id, pw1)
        print("✔ Member registered.")
    except ValueError as e:
        print(e)

def issue_book(data_dir):
    isbn = input("ISBN to issue: ").strip()
    member_id = input("Member ID: ").strip()
    books = load_books(data_dir)
    book = next((b for b in books if b.ISBN == isbn), None)
    if not book:
        print("Book not found.")
        return
    if book.CopiesAvailable < 1:
        print("No copies available.")
        return
    members = load_members(data_dir)
    member = next((m for m in members if m.MemberID == member_id), None)
    if not member:
        print("Member not found.")
        return
    loans = load_loans(data_dir)
    loan_id = next_loan_id(loans)
    today = datetime.today().date()
    due = today + timedelta(days=14)
    loan = Loan(
        LoanID=loan_id, ISBN=isbn, MemberID=member_id,
        IssueDate=str(today), DueDate=str(due), ReturnDate=''
    )
    loans.append(loan)
    book.CopiesAvailable -= 1
    save_loans(data_dir, loans)
    save_books(data_dir, books)
    print(f"✔ Book issued. Due on {due.strftime('%d-%b-%Y')}.")

def return_book(data_dir):
    isbn = input("ISBN to return: ").strip()
    member_id = input("Member ID: ").strip()
    loans = load_loans(data_dir)
    for loan in loans:
        if loan.ISBN == isbn and loan.MemberID == member_id and not loan.ReturnDate:
            loan.ReturnDate = str(datetime.today().date())
            books = load_books(data_dir)
            for b in books:
                if b.ISBN == isbn:
                    b.CopiesAvailable += 1
                    save_books(data_dir, books)
                    break
            save_loans(data_dir, loans)
            print("✔ Book returned.")
            return
    print("Active loan not found.")

def overdue_list(data_dir):
    loans = load_loans(data_dir)
    today = datetime.today().date()
    overdue = [
        l for l in loans
        if not l.ReturnDate and datetime.strptime(l.DueDate, '%Y-%m-%d').date() < today
    ]
    if not overdue:
        print("No overdue loans.")
        return
    print(f"{'LoanID':<7} {'ISBN':<15} {'MemberID':<10} {'DueDate':<12}")
    for l in overdue:
        print(f"{l.LoanID:<7} {l.ISBN:<15} {l.MemberID:<10} {l.DueDate:<12}")

def search_catalogue(data_dir):
    keyword = input("Search by title/author: ").strip().lower()
    books = load_books(data_dir)
    results = [
        b for b in books
        if keyword in b.Title.lower() or keyword in b.Author.lower()
    ]
    if not results:
        print("No books found.")
        return
    print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Available':<8}")
    for b in results:
        print(f"{b.ISBN:<15} {b.Title:<30} {b.Author:<20} {b.CopiesAvailable:<8}")

def borrow_book(data_dir, member):
    isbn = input("ISBN to borrow: ").strip()
    books = load_books(data_dir)
    book = next((b for b in books if b.ISBN == isbn), None)
    if not book:
        print("Book not found.")
        return
    if book.CopiesAvailable < 1:
        print("No copies available.")
        return
    loans = load_loans(data_dir)
    loan_id = next_loan_id(loans)
    today = datetime.today().date()
    due = today + timedelta(days=14)
    loan = Loan(
        LoanID=loan_id, ISBN=isbn, MemberID=member.MemberID,
        IssueDate=str(today), DueDate=str(due), ReturnDate=''
    )
    loans.append(loan)
    book.CopiesAvailable -= 1
    save_loans(data_dir, loans)
    save_books(data_dir, books)
    print(f"✔ Book borrowed. Due on {due.strftime('%d-%b-%Y')}.")

def my_loans(data_dir, member):
    loans = load_loans(data_dir)
    my_loans = [l for l in loans if l.MemberID == member.MemberID]
    if not my_loans:
        print("No loans.")
        return
    print(f"{'LoanID':<7} {'ISBN':<15} {'IssueDate':<12} {'DueDate':<12} {'Returned':<10}")
    for l in my_loans:
        returned = l.ReturnDate if l.ReturnDate else 'No'
        print(f"{l.LoanID:<7} {l.ISBN:<15} {l.IssueDate:<12} {l.DueDate:<12} {returned:<10}")

def main():
    parser = argparse.ArgumentParser(description="Library Management System")
    parser.add_argument('--data-dir', default='./data', help="Data directory for CSV files")
    args = parser.parse_args()
    os.makedirs(args.data_dir, exist_ok=True)
    session = {}
    while True:
        print("\n=== Welcome to Library Management System ===")
        print("1. Librarian Login\n2. Member Login\n3. Exit")
        choice = input("> ").strip()
        if choice == '1':
            user = login(args.data_dir, 'librarian')
            if user:
                session['user'] = user
                librarian_menu(args.data_dir, session)
            else:
                print("Login failed.")
        elif choice == '2':
            user = login(args.data_dir, 'member')
            if user:
                session['user'] = user
                member_menu(args.data_dir, session)
            else:
                print("Login failed.")
        elif choice == '3':
            break

if __name__ == '__main__':
    main()
