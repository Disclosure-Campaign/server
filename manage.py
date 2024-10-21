from app.db.create_db import create_db
from app.db.bulk_data.ingest import ingest

if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'create_db_and_ingest':
        create_db()
        ingest()
