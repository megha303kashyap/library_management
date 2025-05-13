from dataclasses import dataclass
from datetime import date

@dataclass
class Book:
    ISBN: str
    Title: str
    Author: str
    CopiesTotal: int
    CopiesAvailable: int

@dataclass
class Member:
    MemberID: str
    Name: str
    PasswordHash: str  # bcrypt hash
    Email: str
    JoinDate: str

@dataclass
class Loan:
    LoanID: str
    ISBN: str
    MemberID: str
    IssueDate: str  # YYYY-MM-DD
    DueDate: str    # YYYY-MM-DD
    ReturnDate: str # '' if not returned