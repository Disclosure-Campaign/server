# server
pipreqs .

To run locally:

  - Install dependencies:
    - Run `pip install -r requirements.txt`
  - Get environment variables:
    - Obtain .env file and add it to the top folder
  - Database setup:
    - Local option:
      - Ensure that you have psql set up and running locally
      - Run `python manage.py create_db_and_ingest`
      - Make sure `'http://localhost:3000'` is not commented out in app/__init__.py
    - Deployed option:
      - Set FLASK_ENV=development in .env
  - Run server:
    - Run `python run.py`