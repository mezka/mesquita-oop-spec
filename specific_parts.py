from base_classes import IntumescentSeal, Hinge, Core
from odoo_mixins import OdooMixin


class IntumescentSeal10x1(IntumescentSeal, OdooMixin):
    INTERNAL_CODE = 'BURLETE_INTUMESCENTE_10_1'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

    def get_name(self) -> str:
        return "Intumescent Seal 10x1"

    def get_default_code(self) -> str:
        return self.INTERNAL_CODE

    def get_uom(self) -> str:
        return "meter"


class LiteHingeRight(Hinge, OdooMixin):
    INTERNAL_CODE = 'RC212D'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

    def get_name(self) -> str:
        return "Lite Hinge Right"

    def get_default_code(self) -> str:
        return self.INTERNAL_CODE



class LiteHingeLeft(Hinge, OdooMixin):
    INTERNAL_CODE = 'RC212I'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

    def get_name(self) -> str:
        return "Lite Hinge Left"

    def get_default_code(self) -> str:
        return self.INTERNAL_CODE


class FireproofPanel(Core, OdooMixin):
    INTERNAL_CODE = 'AB125'
    WIDTH = 1200
    LENGTH = 1000
    THICKNESS = 50

    def __init__(self):
        super().__init__(
            internal_code=self.INTERNAL_CODE,
            width=self.WIDTH,
            length=self.LENGTH,
            thickness=self.THICKNESS
        )

    def get_name(self) -> str:
        return f"Fireproof Panel {self.THICKNESS}mm"

    def get_default_code(self) -> str:
        return self.INTERNAL_CODE
