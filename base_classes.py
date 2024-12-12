from .attributes import Grampa
from .calculate_bend_allowance_solidworks import calculate_bend_allowance_with_radius_multiplier
from typing import Dict, Tuple, Union, Optional
from abc import ABC
from .odoo_mixins3 import OdooMixin, OdooAssemblyMixin

type OdooDefaultCode = str


class Component(OdooMixin):
    """Base class for all parts - both basic components and assemblies"""
    def get_attributes(self) -> Dict:
        """Get component attributes excluding components dict"""
        return {
            key: value for key, value in self.__dict__.items() 
            if key != 'components'
        }

class Assembly(Component, OdooAssemblyMixin):
    """Class for parts that can contain other components"""
    def __init__(self):
        self.components: Dict[str, Tuple[int, Component]] = {}
        
    def show_components(self, indent: int = 0, is_last: bool = True) -> None:
        """Display component tree structure"""
        if indent == 0:
            name = self.__class__.__name__
            attrs = self.get_attributes()
            attr_string = f" ({', '.join(f'{k}: {v}' for k, v in attrs.items())})" if attrs else ""
            print(f"{name}{attr_string}")
            
        items = list(self.components.items())
        
        for idx, (name, (qty, comp)) in enumerate(items):
            tree_char = "└── " if idx == len(items) - 1 else "├── "
            indentation = "    " * indent
            
            attrs = comp.get_attributes()
            attr_string = f" ({', '.join(f'{k}: {v}' for k, v in attrs.items())})" if attrs else ""
            print(f"{indentation}{tree_char}{qty}x {name}{attr_string}")
            
            # If component has subcomponents, show them
            if isinstance(comp, Assembly):
                comp.show_components(indent + 1, idx == len(items) - 1)

class Core(Component):
    def __init__(self, default_code: OdooDefaultCode, width: float, length: float, thickness: float):
        self.default_code = default_code
        self.width = width
        self.length = length
        self.thickness = thickness

    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")

    def get_default_code(self) -> OdooDefaultCode:
        return self.default_code

    
class WallPlate(Component):
    def __init__(self, default_code:OdooDefaultCode):
        self.default_code = default_code

    def get_name(self) -> str:
        return self.default_code
    
    def get_default_code(self) -> OdooDefaultCode:
        return self.default_code
    

class Hinge(Component):
    def __init__(self, default_code: OdooDefaultCode):
        self.default_code = default_code
    
    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")
    
    def get_default_code(self) -> OdooDefaultCode:
        return self.default_code

class IntumescentSeal(Component):
    def __init__(self, default_code: OdooDefaultCode):
        self.default_code = default_code

    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")
    
    def get_default_code(self) -> OdooDefaultCode:
        return self.default_code

class SheetMetalCut(Component):
    def __init__(self, width: float, height:float, thickness:float):
        self.width = width
        self.height = height
        self.thickness = thickness

    def get_default_code(self) -> OdooDefaultCode:
        return f'Z_CORTE_DE_CHAPA_{self.width}_{self.height}_{self.thickness}'
    
    def get_name(self) -> str:
        return f'Corte de chapa {self.width}x{self.height}x{self.thickness}'

class BendSingleDoorLeafBase(Assembly):
    def __init__(self, external_width_body: float, external_height_body: float, internal_depth: float, assembly_flange_width: float , sheet_metal_thickness: float):
        
        super().__init__()

        self.external_width_body = external_width_body
        self.external_height_body = external_height_body
        self.internal_depth = internal_depth
        self.assembly_flange_width = assembly_flange_width
        self.sheet_metal_thickness = sheet_metal_thickness

        bend_allowance_90_deg = calculate_bend_allowance_with_radius_multiplier(bend_angle=90, thickness = sheet_metal_thickness, bend_radius_multiplier=1)

        sheet_metal_cut_width = external_width_body + internal_depth * 2 + assembly_flange_width * 2 + bend_allowance_90_deg * 4
        sheet_metal_cut_height = external_height_body + internal_depth * 2 + assembly_flange_width * 2 + bend_allowance_90_deg * 4

        self.components['sheet_metal_cut'] = (1, SheetMetalCut(sheet_metal_cut_width, sheet_metal_cut_height, sheet_metal_thickness))


        def get_default_code(self) -> str:
            return f'Z_PLEGADO_CAJON_{self.external_width_body}_{self.external_height_body}_{self.internal_depth}_{self.assembly_flange_width}_{self.sheet_metal_thickness}'
    
        def get_name(self) -> OdooDefaultCode:
            return f'Plegado cajon {self.external_width_body}_{self.external_height_body}_{self.internal_depth}_{self.assembly_flange_width}_{self.sheet_metal_thickness}'

class BendSingleDoorLeafCover(Assembly):
    def __init__(self, external_face_width:float, external_face_height:float, return_flange_width: float, sheet_metal_thickness:float):

        super().__init__()

        bend_allowance_0_deg = calculate_bend_allowance_with_radius_multiplier(bend_angle=0, thickness=sheet_metal_thickness, bend_radius_multiplier=1.5)
        
        sheet_metal_cut_width = external_face_width + 2 * return_flange_width + 2 * bend_allowance_0_deg
        sheet_metal_cut_height = external_face_height + 2 * return_flange_width + 2 * bend_allowance_0_deg

        self.external_face_width = external_face_width
        self.external_face_height = external_face_height
        self.sheet_metal_thickness = sheet_metal_thickness

        self.components['sheet_metal_cut'] = (1, SheetMetalCut(sheet_metal_cut_width, sheet_metal_cut_height, sheet_metal_thickness))

        def get_default_code(self) -> str:
            return f'Z_PLEGADO_TAPA_{self.external_face_width}_{self.external_face_height}_{self.sheet_metal_thickness}'
    
        def get_name(self) -> OdooDefaultCode:
            return f'Plegado tapa {self.external_face_width}x{self.external_face_height}x{self.sheet_metal_thickness}'

class BendUChannel(Assembly):
    def __init__(self, external_width: float, external_length:float, sheet_metal_thickness:float):
        
        super().__init__()

        self.external_width = external_width
        self.external_length = external_length
        self.sheet_metal_thickness = sheet_metal_thickness

        bend_allowance_90_deg = calculate_bend_allowance_with_radius_multiplier(bend_angle=90, thickness=sheet_metal_thickness, bend_radius_multiplier=1)

        sheet_metal_width = external_width + external_length * 2 + bend_allowance_90_deg * 2
        sheet_metal_height = external_length

        self.components['sheet_metal_cut'] = (1, SheetMetalCut(sheet_metal_width, sheet_metal_height, sheet_metal_thickness))

    def get_default_code(self) -> str:
        return f'Z_PLEGADO_PERFIL_U_{self.external_width}_{self.external_length}_{self.sheet_metal_thickness}'

    def get_name(self) -> str:
        return f'Plegado perfil U {self.external_width}x{self.external_length}x{self.sheet_metal_thickness}'


class SingleDoorLeaf(Assembly):
    def __init__(self, bend_single_door_leaf_base: BendSingleDoorLeafBase, bend_single_door_leaf_cover: BendSingleDoorLeafCover, core: Core):

        super().__init__()

        self.components['bend_single_door_leaf_base'] = (1, bend_single_door_leaf_base)
        self.components['bend_single_door_leaf_cover'] = (1, bend_single_door_leaf_cover)
        self.components['core'] = (1, core)

        u_channel_width = 1
        u_channel_length = 1
        u_channel_sheet_metal_thickness = 0.9

        self.components['bend_u_channel'] = (1, BendUChannel(external_width = u_channel_width, external_length=u_channel_length, sheet_metal_thickness=u_channel_sheet_metal_thickness))

    def get_perimeter_without_bottom_edge(self) -> float:

        bend_single_door_leaf_base_body_width = self.components['bend_single_door_leaf_base'][1].external_width_body
        bend_single_door_leaf_base_body_height = self.components['bend_single_door_leaf_base'][1].external_height_body

        return bend_single_door_leaf_base_body_width + 2 * bend_single_door_leaf_base_body_height

    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")
        
    def get_default_code(self) -> OdooDefaultCode:
        raise NotImplementedError("Subclass must implement get_default_code")

class ProfileFrameDoubleRabbet(Assembly):
    def __init__(self, length: float, frame_backbend: float, frame_face: float, 
                 frame_stop: float, frame_soffit: float, frame_rabbet_fixed: float,
                 frame_rabbet_for_leaf: float, sheet_metal_thickness: float):
        
        super().__init__()

        self.length = length
        
        bend_allowance = calculate_bend_allowance_with_radius_multiplier(
            90, sheet_metal_thickness, 1
        )

        dimensions = [frame_backbend, frame_face, frame_stop, 
                     frame_soffit, frame_rabbet_fixed]
        
        sheet_metal_width = (sum(dimensions) + 
                           frame_rabbet_for_leaf + 
                           (len(dimensions) + 1) * bend_allowance)
        
        self.components['sheet_metal_cut'] = (
            1, 
            SheetMetalCut(sheet_metal_width, length, sheet_metal_thickness)
        )

        def get_default_code(self) -> str:
            return f'Z_PLEGADO_PERFIL_MARCO_{self.frame_rabbet_for_leaf}_{self.sheet_metal_thickness}'
    
        def get_name(self) -> OdooDefaultCode:
            return f'Plegado perfil marco {self.frame_rabbet_for_leaf}x{self.sheet_metal_thickness}'

class ProfileFrameDoubleRabbetWithBackbendReturn(Assembly):
    def __init__(self, length: float, frame_backbend_return: float, frame_backbend: float, 
                 frame_face: float, frame_stop: float, frame_soffit: float, 
                 frame_rabbet_fixed: float, frame_rabbet_for_leaf: float, 
                 sheet_metal_thickness: float):
        
        super().__init__()

        self.length = length
        
        bend_allowance = calculate_bend_allowance_with_radius_multiplier(
            90, sheet_metal_thickness, 1
        )
        
        dimensions = [frame_backbend_return, frame_backbend, frame_face, 
                     frame_stop, frame_soffit, frame_rabbet_fixed]
        
        sheet_metal_width = (sum(dimensions) + 
                           frame_rabbet_for_leaf + 
                           (len(dimensions) + 1) * bend_allowance)
        
        self.components['sheet_metal_cut'] = (
            1, 
            SheetMetalCut(sheet_metal_width, length, sheet_metal_thickness)
        )

        def get_default_code(self) -> str:
            return f'Z_PLEGADO_PERFIL_MARCO_{self.frame_rabbet_for_leaf}_{self.sheet_metal_thickness}'
    
        def get_name(self) -> OdooDefaultCode:
            return f'Plegado perfil marco {self.frame_rabbet_for_leaf}x{self.sheet_metal_thickness}'

DoubleRabbetProfileFrameTypes = Union[ProfileFrameDoubleRabbet, ProfileFrameDoubleRabbetWithBackbendReturn]

class DoorFrameDoubleRabbet(Assembly):
    def __init__(self, lintel: DoubleRabbetProfileFrameTypes, 
                 jamb: DoubleRabbetProfileFrameTypes,
                 grampa: Grampa):
        
        super().__init__()
        
        self.components['lintel'] = (1, lintel)
        self.components['jamb'] = (2, jamb)
        self.components['wall_plate'] = (6, WallPlate(grampa.value))
    
    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")
    
    def get_default_code(self) -> str:
        raise NotImplementedError("Subclass must implement get_default_code")

class SingleDoor(Assembly):
    def __init__(self, door_leaf: SingleDoorLeaf, 
                 door_frame: DoorFrameDoubleRabbet,
                 hinges: tuple[int, Hinge],
                 intumescent_seal: Optional[IntumescentSeal] = None):
        
        super().__init__()
        
        self.components['door_leaf'] = (1, door_leaf)
        self.components['door_frame'] = (1, door_frame)
        self.components['hinges'] = hinges
        
        if intumescent_seal:
            self.components['intumescent_seal'] = (self.calculate_required_intumescent_seal_metres(), intumescent_seal)
    
    def calculate_required_intumescent_seal_metres(self):
        perimeter_without_bottom_edge_mm = self.components['door_leaf'][1].get_perimeter_without_bottom_edge()
        perimeter_without_bottom_edge_metres = perimeter_without_bottom_edge_mm / 1000

        return perimeter_without_bottom_edge_metres
    
    def get_name(self) -> str:
        raise NotImplementedError("Subclass must implement get_name")
    
    def get_default_code(self) -> str:
        raise NotImplementedError("Subclass must implement get_default_code")