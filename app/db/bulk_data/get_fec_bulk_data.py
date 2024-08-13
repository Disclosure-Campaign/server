import requests
import zipfile

from io import BytesIO

def fetch_bulk_data(year):
    download_url = f'https://www.fec.gov/files/bulk-downloads/{year}/cn24.zip'

    zip_response = requests.get(download_url)
    zip_response.raise_for_status()

    with zipfile.ZipFile(BytesIO(zip_response.content)) as z:
        z.extractall('app/db/bulk_data')

fetch_bulk_data(2024)