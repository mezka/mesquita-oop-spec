from generate_dimension_attribute_mixin import generate_dimension_attribute_mixin
from attributes import Acabado, Grampa, Marco, Sentido

width_mixin_puerta_simple = generate_dimension_attribute_mixin('ANCHO PL', 500, 1100, 50, 100)
width_mixin_puerta_doble = generate_dimension_attribute_mixin('ANCHO PL', 1100, 2200, 50, 100)
height_mixin = generate_dimension_attribute_mixin('ALTO PL', 500, 2400, 50, 50)
acabado_mixin = Acabado.to_attribute_config_mixin(display_type='radio')
marco_mixin = Marco.to_attribute_config_mixin(display_type='radio')
grampa_mixin = Grampa.to_attribute_config_mixin(display_type='radio')
sentido_mixin = Sentido.to_attribute_config_mixin(display_type='radio')


product_template_rf30_lite_simple = {
    'id': 'product_template_rf_30_lite_simple',
    'default_code': 'product_template_rf_30_lite_simple',
    'name': 'PUERTA RF30 LITE SIMPLE',
    'description': 'PUERTA RF30 LITE SIMPLE',
    'is_custom_door': 'TRUE',
    'uom_id/id': 'uom.product_uom_unit',
    'uom_po_id/id': 'uom.product_uom_unit',
    'route_ids/id': 'mrp.route_warehouse0_manufacture',
    'attributes': [width_mixin_puerta_simple, height_mixin, acabado_mixin, marco_mixin, grampa_mixin, sentido_mixin]
}