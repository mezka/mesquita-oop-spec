from attributes import Sentido, TipoDeMarco, Grampa

class Componente:
    def mostrar_componentes(self):

        print(f"----- {self.__class__} -----")

        for key, value in self.__dict__.items():
            if(key != 'componentes'):
                print(f"{key}: {value}")

        if hasattr(self, 'componentes'):
            for key, value in self.componentes.items():

                print(key, value)
                if(value[1].mostrar_componentes):
                    value[1].mostrar_componentes()

class PanelDeRelleno(Componente):
    def __init__(self, codigo):
        self.codigo = codigo

class Bisagra(Componente):
    def __init__(self, codigo: int):
        self.codigo = codigo

class Burlete(Componente):
    def __init__(self, ancho: int, espesor:int):
        self.ancho = ancho
        self.espesor = espesor

class CorteDeChapa(Componente):
    def __init__(self, ancho: int, alto:int, espesor:int):
        self.ancho = ancho
        self.alto = alto
        self.espesor = espesor

class Cajon(Componente):
    def __init__(self, ancho_ext_cuerpo: int, alto_ext_cuerpo: int, ancho_solapa: int, profundidad_interior: int, espesor_de_chapa: int):
        self.componentes = {}

        self.ancho_ext_cuerpo = ancho_ext_cuerpo
        self.profundidad_interior = profundidad_interior

        self.componentes['corte_de_chapa'] = (1, CorteDeChapa(100, 200, espesor_de_chapa))

class Tapa(Componente):
    def __init__(self, espesor_de_chapa:float, ancho_ext=None, alto_ext=None):

        self.componentes = {}
        self.componentes['corte_de_chapa'] = (1, CorteDeChapa(100, 200, espesor_de_chapa))

class PerfilU(Componente):
    def __init__(self, ancho_ext: int, alto_ext:int):
        self.componentes = {}
        self.componentes['corte_de_chapa'] = (1, CorteDeChapa(100, 200, 0.9))

class Hoja(Componente):
    def __init__(self, cajon: Cajon, tapa: Tapa):

        self.componentes = {}

        self.componentes['cajon'] = (1, cajon)
        self.componentes['tapa'] = (1, tapa)
        self.componentes['relleno'] = (1, PanelDeRelleno(123))

        perfil_u_ancho = cajon.ancho_ext_cuerpo
        perfil_u_alto = cajon.profundidad_interior

        self.componentes['perfil_u'] = (1, PerfilU(ancho_ext = perfil_u_ancho, alto_ext=perfil_u_alto))

class PerfilMarcoAmericano(Componente):
    def __init__(self, largo_ext, tipo_de_marco:TipoDeMarco, espesor_de_chapa: float, descanso_para_hoja: int):
        self.componentes = {}
        self.componentes['corte_de_chapa'] = (1, CorteDeChapa(100, 200, espesor_de_chapa))

class Marco(Componente):
    def __init__(self, ancho_mt: int, alto_mt: int, tipo_de_marco: TipoDeMarco, espesor_de_chapa: float, descanso_para_hoja: int):

        self.componentes = {}

        self.componentes['dintel'] = (1, PerfilMarcoAmericano(largo_ext=ancho_mt, tipo_de_marco=tipo_de_marco, espesor_de_chapa=espesor_de_chapa, descanso_para_hoja=descanso_para_hoja))
        self.componentes['jamba'] = (2, PerfilMarcoAmericano(largo_ext=alto_mt, tipo_de_marco=tipo_de_marco, espesor_de_chapa=espesor_de_chapa, descanso_para_hoja=descanso_para_hoja))

class PuertaSimpleLite(Componente):

    ESPECIFICACION = {
        'HOJA': {
            'TAPA': {                
                'variacion_dimensional_pieza_con_ancho_paso_libre': 10,
                'variacion_dimensional_pieza_con_alto_paso_libre': 10,
                'variacion_dimensional_retazo_con_ancho_paso_libre': 10,
                'variacion_dimensional_retazo_con_alto_paso_libre': 10,
                'espesor_de_chapa': 0.9
            },
            'CAJON': {
                'ancho_solapa': 5,
                'profundidad_interior': 50,
                'espesor_de_chapa': 0.9
            },
            'RELLENO': {
                'ancho': 1200,
                'alto': 1000,
                'espesor': 50,
                'codigo': 'AB125'
            }
        },
        'MARCO': {
            'espesor_de_chapa': 1.2,
            'descanso_para_hoja': 52
        },
        'BISAGRA': {
            Sentido.IZQUIERDA.name: 'RC252I',
            Sentido.DERECHA.name: 'RC252D'
        }
    }

    def __init__(self, ancho_pl: int, alto_pl: int, sentido: Sentido, tipo_de_marco: TipoDeMarco, grampa: Grampa):

        self.componentes = {}

        cajon_ancho_solapa = self.__class__.ESPECIFICACION['HOJA']['CAJON']['ancho_solapa']
        cajon_profundidad_interior = self.__class__.ESPECIFICACION['HOJA']['CAJON']['profundidad_interior']
        cajon_espesor_chapa = self.__class__.ESPECIFICACION['HOJA']['CAJON']['espesor_de_chapa']

        tapa_espesor_chapa = self.__class__.ESPECIFICACION['HOJA']['TAPA']['espesor_de_chapa']

        self.componentes['hoja'] = (1, Hoja(cajon=Cajon(ancho_ext_cuerpo = ancho_pl, alto_ext_cuerpo = alto_pl, profundidad_interior=cajon_profundidad_interior, ancho_solapa=1, espesor_de_chapa=cajon_espesor_chapa), tapa=Tapa(espesor_de_chapa=tapa_espesor_chapa)))

        marco_lite_descanso_para_hoja = cajon_profundidad_interior + cajon_espesor_chapa
        marco_lite_espesor_de_chapa = self.__class__.ESPECIFICACION['MARCO']['espesor_de_chapa']
        self.componentes['marco'] = (1, Marco(ancho_mt=ancho_pl + 100, alto_mt=alto_pl + 50, tipo_de_marco=TipoDeMarco, espesor_de_chapa=marco_lite_espesor_de_chapa, descanso_para_hoja=marco_lite_descanso_para_hoja))
        
        self.componentes['burlete'] = (5, Burlete(20, 1))
        
        codigo_bisagra_lite = self.__class__.ESPECIFICACION['BISAGRA'][Sentido.IZQUIERDA.name] if Sentido.IZQUIERDA else self.__class__.ESPECIFICACION['BISAGRA'][Sentido.DERECHA.name]
        self.componentes['bisagra'] = (3, Bisagra(codigo_bisagra_lite))


if __name__ == "__main__":
    puerta_simple_lite_900_2000 = PuertaSimpleLite(900, 2000, Sentido.IZQUIERDA, TipoDeMarco.INT_100_EXT_130, Grampa.DURLOCK)
    puerta_simple_lite_900_2000.mostrar_componentes()