from enum import Enum
from typing import Dict

class EnumToOdooProductAttributeMixin:
    @classmethod
    def get_snake_case_class_name(cls) -> str:
        return ''.join('_' + c if c.isupper() else c for c in cls.__name__).lstrip('_').upper()

    @classmethod
    def to_attribute_config_mixin(cls, *, display_type: str, sequence: int = 10) -> Dict:
        attribute_name = cls.get_snake_case_class_name()
        return {
            'product_attribute_name': attribute_name,
            'product_attribute_values': [
                {
                    'id': f'product_attribute_value_{attribute_name.lower()}_{member.name.lower()}',
                    'name': member.value,
                    'attribute_id/id': f'product_attribute_{attribute_name.lower()}',
                    'is_custom': 'FALSE',
                }
                for member in cls
            ],
            'product_attribute_display_type': display_type,
            'sequence': str(int(sequence)),
        }

class BaseEnum(EnumToOdooProductAttributeMixin, str, Enum):
    pass

class Sentido(BaseEnum):
    IZQUIERDA = 'IZQUIERDA'
    DERECHA = 'DERECHA'

class Marco(BaseEnum):
    INT_100_EXT_130 = 'INT_100_EXT_130'
    INT_120_EXT_150 = 'INT_120_EXT_150'
    INT_140_EXT_170 = 'INT_140_EXT_170'
class Grampa(BaseEnum):
    DURLOCK = 'DURLOCK'
    MAMPOSTERIA = 'MAMPOSTERIA'

class Acabado(BaseEnum):
    SIN_PINTAR = 'SIN_PINTAR'
    IMPRESION_GRIS = 'IMPRESION_GRIS'
    IMPRESION_BLANCA = 'IMPRESION_BLANCA'
    IMPRESION_ROJA = 'IMPRESION_ROJA'