from odoo import models, fields
from ..mesquita_environment import MesquitaEnvironment
from ..lite import LiteSingleDoor
from ..attributes import Sentido, Marco, Grampa
import logging

_logger = logging.getLogger(__name__)

class CustomProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_custom_door = fields.Boolean(string='Is Custom Door', default=False)

    def _get_door_attributes(self, combination):

        attr_values = self.env['product.template.attribute.value'].browse(combination.ids)

        values = {}
        for attr_value in attr_values:
            attribute_name = attr_value.attribute_id.name
            value_name = attr_value.product_attribute_value_id.name
            values[attribute_name] = value_name

        return values

    def _create_product_variant(self, combination, log_warning=False):
        """Override the variant creation method to handle custom door variants"""
        _logger.error('CustomProductTemplate._create_product_variant: Entering _create_product_variant method')
        created_product_product = super()._create_product_variant(combination=combination,log_warning=False)
        self.env.cr.commit()

        if created_product_product.product_tmpl_id.is_custom_door:

            _logger.error('Inside door custom')
            attr_values = self._get_door_attributes(combination)
            # try:
            ancho_pl = int(attr_values.get('ANCHO PL'))
            alto_pl = int(attr_values.get('ALTO PL'))
            sentido = Sentido[attr_values.get('SENTIDO')]
            marco = Marco[attr_values.get('MARCO')]
            grampa = Grampa[attr_values.get('GRAMPA')]

            with MesquitaEnvironment(self.env):
                door = LiteSingleDoor(
                    ancho_pl=ancho_pl,
                    alto_pl=alto_pl,
                    sentido=sentido,
                    marco=marco,
                    grampa=grampa
                )

                door.save_to_odoo(created_product_product.product_tmpl_id.id, created_product_product.id)

            # except Exception as e:
            #     _logger.error(f'Error creating door variant: {e}')
            #     return created_product_product

        return created_product_product