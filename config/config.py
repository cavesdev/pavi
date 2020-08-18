"""
Configuration Class that holds all the required configuration variables.
Shared between various modules inside the program.
"""

import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    __conf = {
        'dev': os.getenv('FLASK_ENV') != 'production',
        'port': os.getenv('PORT') or 3000,
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_name': os.getenv('DB_NAME'),
        'db_collection': os.getenv('DB_COLLECTION')
    }

    @staticmethod
    def get(name):
        """
        Get configuration variable
        :param name: the configuration value to get
        """
        return Config.__conf[name]
