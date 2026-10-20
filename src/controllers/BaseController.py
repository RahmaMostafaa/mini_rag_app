from helpers.config import get_settings ,Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        #to locate Assets files from base
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        
       
        # assets/files directory
        self.files_dir = os.path.join(
            self.base_dir,
            "assets",
            "files"
        )

        #for vectordb to path_db path
        self.database_dir = os.path.join(
        self.base_dir,
        "assets",
        "database"
    )



    def generate_random_string(self, lenght: int=12): #random char+num
        return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))
    
    def get_database_path(self, db_name: str):

        database_path = os.path.join(
        self.database_dir, db_name
        )

        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path
