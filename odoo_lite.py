from typing import Any
from odoo_mixins import OdooMixin, OdooAssemblyMixin
from lite import (
    LiteSingleDoor, LiteProfileFrameDoubleRabbet100, 
    LiteProfileFrameDoubleRabbet120, LiteProfileFrameDoubleRabbet140,
    LiteBendSingleDoorLeafBase, LiteBendSingleDoorLeafCover,
    LiteSingleDoorLeaf, LiteDoorFrameDoubleRabbet
)
from specific_parts import (
    FireproofPanel, LiteHingeRight, LiteHingeLeft, 
    IntumescentSeal10x1
)

class OdooFireproofPanel(FireproofPanel, OdooMixin):
    def get_name(self) -> str:
        return f"Fireproof Panel {self.thickness}mm"
        
    def get_internal_reference(self) -> str:
        return self.internal_code
        
    def get_type(self) -> str:
        return "product"

class OdooLiteHingeRight(LiteHingeRight, OdooMixin):
    def get_name(self) -> str:
        return "Lite Hinge Right"
        
    def get_internal_reference(self) -> str:
        return self.internal_code
        
    def get_type(self) -> str:
        return "product"

class OdooLiteHingeLeft(LiteHingeLeft, OdooMixin):
    def get_name(self) -> str:
        return "Lite Hinge Left"
        
    def get_internal_reference(self) -> str:
        return self.internal_code
        
    def get_type(self) -> str:
        return "product"

class OdooIntumescentSeal10x1(IntumescentSeal10x1, OdooMixin):
    def get_name(self) -> str:
        return "Intumescent Seal 10x1"
        
    def get_internal_reference(self) -> str:
        return self.internal_code
        
    def get_type(self) -> str:
        return "product"

# Profile Frame assemblies
class OdooLiteProfileFrameDoubleRabbet100(LiteProfileFrameDoubleRabbet100, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Profile Frame Double Rabbet 100 L={self.length}mm"
        
    def get_internal_reference(self) -> str:
        return f"LITE-FRAME-100-{self.length}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteProfileFrameDoubleRabbet120(LiteProfileFrameDoubleRabbet120, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Profile Frame Double Rabbet 120 L={self.length}mm"
        
    def get_internal_reference(self) -> str:
        return f"LITE-FRAME-120-{self.length}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteProfileFrameDoubleRabbet140(LiteProfileFrameDoubleRabbet140, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Profile Frame Double Rabbet 140 L={self.length}mm"
        
    def get_internal_reference(self) -> str:
        return f"LITE-FRAME-140-{self.length}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteBendSingleDoorLeafBase(LiteBendSingleDoorLeafBase, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Bend Single Door Leaf Base {self.external_width_body}x{self.external_height_body}"
        
    def get_internal_reference(self) -> str:
        return f"LITE-BASE-{self.external_width_body}x{self.external_height_body}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteBendSingleDoorLeafCover(LiteBendSingleDoorLeafCover, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Bend Single Door Leaf Cover {self.external_face_width}x{self.external_face_height}"
        
    def get_internal_reference(self) -> str:
        return f"LITE-COVER-{self.external_face_width}x{self.external_face_height}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteSingleDoorLeaf(LiteSingleDoorLeaf, OdooAssemblyMixin):
    def get_name(self) -> str:
        base = self.components['bend_single_door_leaf_base'][1]
        return f"Lite Single Door Leaf {base.external_width_body}x{base.external_height_body}"
        
    def get_internal_reference(self) -> str:
        base = self.components['bend_single_door_leaf_base'][1]
        return f"LITE-LEAF-{base.external_width_body}x{base.external_height_body}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteDoorFrameDoubleRabbet(LiteDoorFrameDoubleRabbet, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Door Frame Double Rabbet {self.components['lintel'][1].length}"
        
    def get_internal_reference(self) -> str:
        return f"LITE-FRAME-{self.components['lintel'][1].length}"
        
    def get_type(self) -> str:
        return "product"

class OdooLiteSingleDoor(LiteSingleDoor, OdooAssemblyMixin):
    def get_name(self) -> str:
        return f"Lite Single Door {self.ancho_pl}x{self.alto_pl} {self.sentido.name} {self.marco.name}"
        
    def get_internal_reference(self) -> str:
        return f"LITE-DOOR-{self.ancho_pl}x{self.alto_pl}-{self.sentido.name}-{self.marco.name}"
        
    def get_type(self) -> str:
        return "product"