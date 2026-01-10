from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["sales_dialer"]

managers = db.managers
salespersons = db.salespersons
leads = db.leads
calls = db.calls
followups = db.followups
