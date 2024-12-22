
import os


class Settings:
    in_database: bool = os.environ.get('IN_DATABASE', 'true').lower() == 'true'
