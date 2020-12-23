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
        'port': os.getenv('PORT') or 5000,
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_name': os.getenv('DB_NAME'),
        'db_collection': os.getenv('DB_COLLECTION'),
        'upload_folder': os.getenv('UPLOAD_FOLDER') or os.path.join('static', 'videos'),
        'upload_size_limit': 100 * 1024 * 1024 # 100MB
    }

    @staticmethod
    def get(name):
        """
        Get configuration variable
        :param name: the configuration value to get
        """
        return Config.__conf[name]
