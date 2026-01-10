import bcrypt
from backend.config.db import managers, salespersons

# Clear old users
managers.delete_many({})
salespersons.delete_many({})

# Hash password
password = bcrypt.hashpw("1234".encode(), bcrypt.gensalt())

# Insert Manager
managers.insert_one({
    "email": "manager@test.com",
    "password": password,   # 🔥 hashed bytes
    "name": "Test Manager",
    "role": "manager"
})

# Insert Salesperson
salespersons.insert_one({
    "email": "sales@test.com",
    "password": password,   # 🔥 hashed bytes
    "name": "Test Sales",
    "role": "salesperson",
    "managerId": None
})

print("✅ Test users inserted with hashed passwords")
