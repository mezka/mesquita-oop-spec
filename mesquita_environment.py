from .odoo_mixins3 import OdooMixin

class MesquitaEnvironment:
    def __init__(self, env):
        self.env = env
        
    def __enter__(self):
        OdooMixin.env = self.env
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        OdooMixin.env = None