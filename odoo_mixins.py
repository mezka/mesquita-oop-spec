from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class OdooMixin(ABC):
    env = None
        
    @abstractmethod
    def get_name(self) -> str:
        pass
        
    @abstractmethod
    def get_default_code(self) -> str:
        pass

    def get_type(self) -> str:
        return "product"

    def get_uom(self) -> str:
        return "unit"

    def _get_product(self) -> Optional[int]:
        product = self.env['product.product'].search([
            ('default_code', '=', self.get_default_code())
        ], limit=1)
        return product.id if product else None

    def _create_product(self) -> int:
        product = self.env['product.product'].create({
            'name': self.get_name(),
            'default_code': self.get_default_code(),
            'type': self.get_type(),
            'detailed_type': self.get_type(),
            'uom_id': self.env.ref(f'uom.{self.get_uom()}').id,
            'uom_po_id': self.env.ref(f'uom.{self.get_uom()}').id
        })

        return product.id

    def save_to_odoo(self) -> int:
        product_id = self._get_product()
        if not product_id:
            product_id = self._create_product()
        return product_id

class OdooAssemblyMixin(OdooMixin):
    def _get_bom(self, product_id: int):
        return self.env['mrp.bom'].search([
            ('product_id', '=', product_id)
        ], limit=1)

    def _create_bom(self, product_id: int, component_ids: Dict[int, float]):
        product = self.env['product.product'].browse(product_id)
        
        bom_lines = [
            (0, 0, {
                'product_id': comp_id,
                'product_qty': qty
            }) 
            for comp_id, qty in component_ids.items()
        ]
        
        self.env['mrp.bom'].create({
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_id': product_id,
            'type': 'normal',
            'bom_line_ids': bom_lines
        })

    def save_to_odoo(self) -> int:
        component_ids = {}
        
        for qty, component in self.components.values():
            if isinstance(component, OdooMixin):
                component_id = component.save_to_odoo()
                component_ids[component_id] = qty
        
        product_id = super().save_to_odoo()
        
        if component_ids and not self._get_bom(product_id):
            self._create_bom(product_id, component_ids)
            
        return product_id