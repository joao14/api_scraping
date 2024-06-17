import os
from dotenv import load_dotenv

class Settings:
    PROJECT_NAME: str = "ReCaptcha Solver API Excersice"
    VERSION: str = "1.0.0"
    RECAPTCHA_SITE_KEY: str = os.getenv("RECAPTCHA_SITE_KEY")

settings = Settings()