
from flask import current_app
from typing import Optional




class LinkGenerator:
    def __init__(self,base_url: Optional[str] = None):
        self.base_url = base_url or current_app.config['BASE_URL']

    
    def get_base_url(self):
        if self.base_url:
            return self.base_url.rstrip('/')
        return current_app.config['BASE_URL'].rstrip('/')

    def generate_download_link(self, token: str) -> str:
        return f"{self.base_url}/d/{token}"


    def generate_info_link(self, token: str) -> str:
        return f"{self.base_url}/info/{token}"

    
    
