import logging
import os
from pymongo import MongoClient


MONGODB_URI = os.environ.get("MONGODB_URI")


iv = 61165551222307702139499756523313080189136245847334709143845124077457983490157
keypass = b"O\x7f\xefu\xbaX\x19]d\xd1;[\x040\x07\xc9\xcb\xdd\xf3'\x89~\xee\xf8\xa1\xc5\xa6\xdb?f\x00\x12"
expiry_time = os.getenv("EXPIRY_TIME", 30)  # minutes


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "openid email profile"

# MongoDB connection
try:
    client = MongoClient(MONGODB_URI)
    db = client.db_hotel
except Exception as e:
    logging.error(e)
