import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY missing from env variables")

    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY missing from env variables")