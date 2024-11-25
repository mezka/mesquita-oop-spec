from enum import Enum

class Sentido(Enum):
    IZQUIERDA = 'IZQUIERDA'
    DERECHA = 'DERECHA'

class TipoDeMarco(Enum):
    INT_100_EXT_130 = {'interior': 100, 'exterior': 130}
    INT_120_EXT_150 = {'interior': 120, 'exterior': 150}
    INT_140_EXT_170 = {'interior': 140, 'exterior': 170}

class Grampa(Enum):
    DURLOCK = 'DURLOCK'
    MAMPOSTERIA = 'MAMPOSTERIA'