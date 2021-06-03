import os
from getpass import getpass

from werkzeug.security import generate_password_hash

BASE_PATH = os.path.dirname(__file__)

try:
    password = getpass()
    hashed_password = generate_password_hash(password, method="sha256")

    with open(f"{BASE_PATH}/hash.txt", "w", encoding="utf-8") as f:
        f.write(hashed_password)

    print("Task completed successfully.")
except Exception:
    print("An error has occurred.")
