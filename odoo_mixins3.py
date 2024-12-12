from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

type ProductTemplateId = int
type ProductProductId = int
type BomId = int
type OdooXmlId = str
type OdooTypeValue = str
type BaseDoorVariantProductProductId = str

class OdooMixin(ABC):
    env = None

    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_default_code(self) -> str:
        pass

    def get_type(self) -> OdooTypeValue:
        return "consu"

    def get_uom_xml_id(self) -> OdooXmlId:
        return "uom.product_uom_unit"
    
    def _get_product_product_id_by_product_template_id(self, product_template_id) -> Optional[ProductProductId]:
        logger.info(f'OdooMixin._get_product_product_ids_by_product_template_id: {self.get_name()}, {self.get_default_code()}')
        product_product = self.env['product.product'].search([
            ('product_tmpl_id', '=', product_template_id)
        ])

        if product_product and len(product_product.ids) > 1:
            raise ValueError(f"Expected only one product_product id, got {len(product_product.ids)}")

        return product_product.id if product_product else None

    
    def _get_product_template_id_by_default_code(self) -> Optional[ProductTemplateId]:
        logger.info(f'OdooMixin._get_product_template: {self.get_name()}, {self.get_default_code()}')
        product_template = self.env['product.template'].search([('default_code', '=', self.get_default_code())], limit=1)
        return product_template.id if product_template else None

    def _create_product_template(self) -> ProductTemplateId:
        logger.info(f'OdooMixin._create_product_template: {self.get_name()}, {self.get_default_code()}')
        product_template = self.env['product.template'].create({
            'name': self.get_name(),
            'default_code': self.get_default_code(),
            'type': self.get_type(),
            'uom_id': self.env.ref(self.get_uom_xml_id()).id,
            'uom_po_id': self.env.ref(self.get_uom_xml_id()).id,
        })
        self.env.cr.commit()
        return product_template.id

    def _create_product_product(self, product_template_id) -> ProductProductId:
        logger.info(f'OdooMixin._create_product_product: {self.get_name()}, {self.get_default_code()}')
        product = self.env['product.product'].create({
            'product_tmpl_id': product_template_id,
            'default_code': self.get_default_code(),
        })
        self.env.cr.commit()
        return product.id

    def save_to_odoo(self) -> Tuple[ProductTemplateId, ProductProductId]:
        logger.info(f'OdooMixin.save_component: {self.get_name()}, {self.get_default_code()}')
        product_template_id = self._get_product_template_id_by_default_code()
        
        if not product_template_id:
            product_template_id = self._create_product_template()

        product_product_id = self._get_product_product_id_by_product_template_id(product_template_id)

        if not product_product_id:
            product_product_id = self._create_product_product(product_template_id)

        logger.info(f'OdooMixin.save_component: {product_template_id}, {product_product_id}')
        return (product_template_id, product_product_id)

class OdooAssemblyMixin(OdooMixin):
    def is_door(self):
        door_classes = ['SingleDoor', 'DoubleDoor']
        if any(cls.__name__ in door_classes for cls in self.__class__.__mro__):
            return True

    def save_to_odoo(self, assembly_product_template_id: Optional[ProductTemplateId] = None, assembly_product_product_id: Optional[ProductProductId] = None) -> Tuple[ProductTemplateId, ProductProductId]:
        logger.info(f'OdooAssemblyMixin.save_to_odoo: {self.get_name()}, {self.get_default_code()}')
        component_ids = {}
        for name, (qty, component) in self.components.items():
                component_product_template_id, component_product_product_id = component.save_to_odoo()
                component_ids[component_product_product_id] = qty
        
        if not self.is_door():
            assembly_product_template_id, assembly_product_product_id = OdooMixin.save_to_odoo(self)

        bom = self._get_bom(assembly_product_product_id)

        if not bom:
            bom = self._create_bom(product_id=assembly_product_product_id, component_ids=component_ids, product_tmpl_id=assembly_product_template_id)
        
        return assembly_product_template_id, assembly_product_product_id
    
    def _get_bom(self, product_product_id: ProductProductId) -> Optional[BomId]:
        logger.info(f'OdooAssemblyMixin._get_bom: {self.get_name()}, {self.get_default_code()}')
        bom = self.env['mrp.bom'].search([('product_id', '=', product_product_id)])
        if bom and len(bom.ids) > 1:
            raise ValueError(f"Expected only one bom id, got {len(product_product.ids)}")
        return bom.id if bom else None
    
    def _create_bom(self, product_id: int, component_ids: Dict[ProductProductId, float], product_tmpl_id: int) -> BomId:
        logger.info(f'OdooAssemblyMixin._create_bom: {self.get_name()}, {self.get_default_code()}')

        logger.info(f'OdooAssemblyMixin._create_bom: creating BOM lines')

        bom_lines = [
            (0, 0, {
                'product_id': comp_id,
                'product_qty': qty
            })
            for comp_id, qty in component_ids.items()
        ]
        
        self.env.cr.commit()

        logger.info(f'OdooAssemblyMixin._create_bom: creating BOM')

        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product_tmpl_id,  # Use the passed product_tmpl_id
            'product_id': product_id,
            'type': 'normal',
            'bom_line_ids': bom_lines
        })
        self.env.cr.commit()
        return bom.id

