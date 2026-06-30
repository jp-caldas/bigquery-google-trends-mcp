import os

from dotenv import load_dotenv

load_dotenv()


GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")


def validate() -> None:
    if not GOOGLE_CLOUD_PROJECT:
        raise RuntimeError(
            "GOOGLE_CLOUD_PROJECT environment variable is required. "
            "Set it to your GCP project ID or create a .env file."
        )
