import os

from dotenv import load_dotenv

from model.config import Config


class ConfigService:
    def __init__(self, override: bool):
        load_dotenv(dotenv_path='.env', override=override)
        self.config: Config = Config(db_url=os.environ.get('DATABASE_URL'),
                                     openai_api_key=os.environ.get('OPENAI_API_KEY'))
