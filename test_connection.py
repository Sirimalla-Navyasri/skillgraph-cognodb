from database.connection import Database


db = Database()

try:
    db.verify()
    print("Connected to CognoDB successfully!")

except Exception as error:
    print("Database connection failed:")
    print(error)

finally:
    db.close()