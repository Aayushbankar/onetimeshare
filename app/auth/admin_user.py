"""Simple admin user class for Flask-Login (no database needed)."""

from config import Config


class AdminUser:
    """Simple admin user for Flask-Login with config-based auth."""
    
    def __init__(self):
        self.id = 'admin'
        self.username = Config.ADMIN_USERNAME
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
