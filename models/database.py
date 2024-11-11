from pymongo import MongoClient
from dotenv import load_dotenv
import os
# Load biến môi trường từ file .env
load_dotenv()
# Lấy MongoDB URI từ biến môi trường
mongodb_uri = os.getenv("MONGODB_URI")
# Kết nối với MongoDB
client = MongoClient(mongodb_uri)
db = client['socialdb']
embeddings_collection = db['embeddings']
search_results_collection = db['search_results']
users_collection = db['users']
