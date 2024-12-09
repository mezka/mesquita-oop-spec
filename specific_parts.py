from base_classes import IntumescentSeal, Hinge, Core
# from odoo_mixins import OdooMixin

class IntumescentSeal10x1(IntumescentSeal):
    INTERNAL_CODE = 'BURLETE_INTUMESCENTE_10_1'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

    def get_name(self) -> str:
        return self.INTERNAL_CODE

    def get_internal_code(self) -> str:
        return self.INTERNAL_CODE

class LiteHingeRight(Hinge):
    INTERNAL_CODE = 'RC212D'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

class LiteHingeLeft(Hinge):
    INTERNAL_CODE = 'RC212D'

    def __init__(self):
        super().__init__(internal_code=self.INTERNAL_CODE)

    def get_name(self) -> str:
        return self.INTERNAL_CODE

    def get_internal_code(self) -> str:
        return self.INTERNAL_CODE

class FireproofPanel(Core):
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
        return self.INTERNAL_CODE

    def get_internal_code(self) -> str:
        return self.INTERNAL_CODE