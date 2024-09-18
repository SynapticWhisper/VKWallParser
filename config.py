import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN: str = os.environ.get("VK_TOKEN")
API_VERSION: str = os.environ.get("API_VERSION")