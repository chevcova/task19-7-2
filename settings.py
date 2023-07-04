import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

# ключ взятый из Swagger для теста
invalid_auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"}
