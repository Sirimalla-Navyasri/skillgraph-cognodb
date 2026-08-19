from database.connection import Database
from database.queries import GET_CANDIDATES


db = Database()

results = db.query(GET_CANDIDATES)

for candidate in results:
    print(candidate)

db.close()