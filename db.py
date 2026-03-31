import os

MONGO_URL = os.environ.get("MONGO_URL")

class LocalDB:
    def __init__(self):
        self.users = set()
        self.admins = set()

    def is_user_authorized(self, *a, **k): return True
    def is_admin(self, *a, **k): return True

    def __getattr__(self, name):
        return lambda *a, **k: True


try:
    if MONGO_URL:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URL)
        db = client["botdb"]
        print("✅ MongoDB Connected")
    else:
        raise Exception("No MONGO_URL")

except Exception as e:
    print("❌ Mongo Failed → Using Local DB")

    class Database:
        def __init__(self):
            self.local = LocalDB()

        def __getattr__(self, name):
            return getattr(self.local, name)

    db = Database()
