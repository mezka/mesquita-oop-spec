from .base_classes import IntumescentSeal, Hinge, Core
from .odoo_mixins3 import OdooMixin


class IntumescentSeal10x1(IntumescentSeal):
    DEFAULT_CODE = 'BURLETE_INTUMESCENTE_10_1'

    def __init__(self):
        super().__init__(default_code=self.DEFAULT_CODE)

    def get_name(self) -> str:
        return "Intumescent Seal 10x1"

    def get_default_code(self) -> str:
        return self.DEFAULT_CODE

    def get_uom(self) -> str:
        return "meter"


class LiteHingeRight(Hinge):
    DEFAULT_CODE = 'RC212D'

    def __init__(self):
        super().__init__(default_code=self.DEFAULT_CODE)

    def get_name(self) -> str:
        return "Lite Hinge Right"

    def get_default_code(self) -> str:
        return self.DEFAULT_CODE



class LiteHingeLeft(Hinge):
    DEFAULT_CODE = 'RC212I'

    def __init__(self):
        super().__init__(default_code=self.DEFAULT_CODE)

    def get_name(self) -> str:
        return "Lite Hinge Left"

    def get_default_code(self) -> str:
        return self.DEFAULT_CODE


class FireproofPanel(Core):
    DEFAULT_CODE = 'AB125'
    WIDTH = 1200
    LENGTH = 1000
    THICKNESS = 50

    def __init__(self):
        super().__init__(
            default_code=self.DEFAULT_CODE,
            width=self.WIDTH,
            length=self.LENGTH,
            thickness=self.THICKNESS
        )

    def get_name(self) -> str:
        return f"Fireproof Panel {self.THICKNESS}mm"

    
