import bcrypt
import getpass
import csv
from models import Member
from datetime import date

MEMBERS_CSV = 'data/members.csv'

# 🔐 Password Helpers
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# 📥 Load and Save Members
def load_members(file_path=MEMBERS_CSV):
    members = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members.append(Member(**row))
    return members

def save_members(members, file_path=MEMBERS_CSV):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Member.__annotations__.keys())
        writer.writeheader()
        for m in members:
            writer.writerow(m.__dict__)

# 👤 Register Member
def register_member():
    members = load_members()

    member_id = input("New Member ID: ")
    if any(m.MemberID == member_id for m in members):
        print("❌ Member ID already exists.")
        return

    name = input("Name: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    hashed = hash_password(password)
    join_date = str(date.today())

    new_member = Member(MemberID=member_id, Name=name, PasswordHash=hashed,
                        Email=email, JoinDate=join_date)
    members.append(new_member)
    save_members(members)

    print("✅ Member registered successfully.")

# 🔓 Login
def member_login():
    members = load_members()
    member_id = input("Member ID: ")
    password = getpass.getpass("Password: ")

    for m in members:
        if m.MemberID == member_id and verify_password(password, m.PasswordHash):
            print(f"✅ Welcome, {m.Name}!")
            return m  # Logged-in Member object

    print("❌ Invalid credentials.")
    return None

def librarian_login():
    lib_id = input("Librarian ID: ")
    password = getpass.getpass("Password: ")

    if lib_id == 'admin' and password == '123456':
        print(f"✅ Welcome, Librarian!")
        return 'admin'

    print("❌ Invalid credentials.")
    return None
