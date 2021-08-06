"""
Configuration Class that holds all the required configuration variables.
Shared between various modules inside the program.
"""

import os


class Config:
    __conf = {
        'dev': os.getenv('FLASK_ENV') != 'production',
        'port': os.getenv('PORT') or 5000,
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_name': os.getenv('DB_NAME'),
        'db_collection': os.getenv('DB_COLLECTION'),
        'project_path': os.getenv('PROJECT_PATH'),
        'project_module_path': os.getenv('PROJECT_MODULE_PATH'),
        'static_folder': os.path.join(os.getenv('PROJECT_PATH'), 'static'),
        'upload_folder': os.getenv('UPLOAD_FOLDER') or os.path.join(os.getenv('PROJECT_PATH'), 'static', 'videos'),
        'upload_size_limit': os.getenv('UPLOAD_SIZE_LIMIT') or 100 * 1024 * 1024  # 100MB
    }

    @staticmethod
    def get(name):
        """
        Get configuration variable
        :param name: the configuration value to get
        """
        return Config.__conf[name]
