import os

from dotenv import load_dotenv

load_dotenv()

print(set(os.getenv("ALLOWED_EXTENSIONS").split(",")))
