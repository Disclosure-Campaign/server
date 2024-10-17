from app.db.create_db import create_db
from app.db.bulk_data.ingest import ingest

if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'create_db':
        create_db()
    elif sys.argv[1] == 'ingest':
        ingest()
