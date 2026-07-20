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

    def generate_random_string(self, lenght: int=12): #random char+num
        return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))