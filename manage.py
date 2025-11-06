if __name__ == '__main__':
    import sys

    # Import create_db and ingest only when running the manage script
    # This avoids pulling heavy dependencies (pandas) into the web dyno
    # if this module is imported accidentally.
    from app.db.create_db import create_db
    from app.db.bulk_data.ingest import ingest

    if sys.argv[1] == 'create_db_and_ingest':
        create_db()
        ingest()
