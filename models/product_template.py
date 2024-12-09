from odoo import models
from mesquita_environment import MesquitaEnvironment
from odoo_lite import OdooLiteSingleDoor
from attributes import Sentido, Marco, Grampa

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _create_variant_ids(self):
        if self.default_code in ['product_template_rf_30_lite_simple']:
            values = self._get_current_variant_values()
            if values:
                self._create_lite_door_variant(values)
        return super()._create_variant_ids()
    
    def _create_lite_door_variant(self, values):
        ancho_pl = int(values['ANCHO PL'])
        alto_pl = int(values['ALTO PL'])
        sentido = Sentido[values['SENTIDO']]
        marco = Marco[values['MARCO']]
        grampa = Grampa[values['GRAMPA']]
        
        with MesquitaEnvironment(self.env):
            door = OdooLiteSingleDoor(
                ancho_pl=ancho_pl,
                alto_pl=alto_pl,
                sentido=sentido,
                marco=marco,
                grampa=grampa
            )
            door.save_to_odoo()