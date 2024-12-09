from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple

class OdooMixin(ABC):
    """Base mixin for Odoo product creation"""
    env = None
        
    @abstractmethod
    def get_name(self) -> str:
        """Return product name for Odoo"""
        pass
        
    @abstractmethod
    def get_internal_reference(self) -> str:
        """Return internal reference (default_code) for Odoo"""
        pass

    @abstractmethod     
    def get_type(self) -> str:
        """Return product type for Odoo"""
        pass 

    def get_odoo_data(self) -> Dict[str, Any]:
        """Get complete Odoo product data"""
        return {
            "name": self.get_name(),
            "default_code": self.get_internal_reference(),
            "type": self.get_type(),
            "detailed_type": self.get_type()
        }

    def ensure_product_exists(self) -> int:
        """Ensure product exists in Odoo"""
        product = self.env['product.template'].search(
            [('default_code', '=', self.get_internal_reference())], 
            limit=1
        )
        if not product:
            product = self.env['product.template'].create(self.get_odoo_data())
        return product.id

class OdooAssemblyMixin(OdooMixin):
    """Mixin for assemblies that need BOMs"""
    
    def _create_bom_lines(self) -> List[Tuple[int, int, Dict[str, Any]]]:
        """Create BOM lines from components dict"""
        lines = []
        # We know components exists because this mixin should only be used with Assembly classes
        for name, (qty, component) in self.components.items():
            if isinstance(component, OdooMixin):
                # Ensure component product exists and get its ID
                product_id = component.ensure_product_exists()
                lines.append((0, 0, {
                    'product_id': product_id,
                    'product_qty': qty
                }))
        return lines
    
    def ensure_bom_exists(self, product_id: int):
        """Ensure BOM exists for product"""
        bom = self.env['mrp.bom'].search([
            ('product_tmpl_id', '=', product_id)
        ], limit=1)
        
        if not bom:
            self._create_bom(product_id)
    
    def _create_bom(self, product_id: int):
        """Create BOM record"""
        self.env['mrp.bom'].create({
            'product_tmpl_id': product_id,
            'type': 'normal',
            'bom_line_ids': self._create_bom_lines()
        })

    def save_to_odoo(self):
        """Main method to create/update product and BOM"""
        product_id = self.ensure_product_exists()
        self.ensure_bom_exists(product_id)
        return product_id