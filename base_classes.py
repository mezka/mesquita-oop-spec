from attributes import Grampa
from calculate_bend_allowance_solidworks import calculate_bend_allowance_with_radius_multiplier
from typing import Dict, Tuple, Union, Optional
from abc import ABC

class Component(ABC):
    """Base class for all parts - both basic components and assemblies"""
    def get_attributes(self) -> Dict:
        """Get component attributes excluding components dict"""
        return {
            key: value for key, value in self.__dict__.items() 
            if key != 'components'
        }

class Assembly(Component):
    """Class for parts that can contain other components"""
    def __init__(self):
        super().__init__()
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
    def __init__(self, internal_code: str, width: float, length: float, thickness: float):
        self.internal_code = internal_code
        self.width = width
        self.length = length
        self.thickness = thickness
    
class WallPlate(Component):
    def __init__(self, internal_code:str):
        self.internal_code = internal_code

class Hinge(Component):
    def __init__(self, internal_code: str):
        self.internal_code = internal_code

class IntumescentSeal(Component):
    def __init__(self, internal_code: str):
        self.internal_code = internal_code

class SheetMetalCut(Component):
    def __init__(self, width: float, height:float, thickness:float):
        self.width = width
        self.height = height
        self.thickness = thickness

class BendSingleDoorLeafBase(Assembly):
    def __init__(self, external_width_body: float, external_height_body: float, internal_depth: float, assembly_flange_width: float , sheet_metal_thickness: float):
        
        super().__init__()

        self.external_width_body = external_width_body
        self.internal_depth = internal_depth

        bend_allowance_90_deg = calculate_bend_allowance_with_radius_multiplier(bend_angle=90, thickness = sheet_metal_thickness, bend_radius_multiplier=1)

        sheet_metal_cut_width = external_width_body + internal_depth * 2 + assembly_flange_width * 2 + bend_allowance_90_deg * 4
        sheet_metal_cut_height = external_height_body + internal_depth * 2 + assembly_flange_width * 2 + bend_allowance_90_deg * 4

        self.components['sheet_metal_cut'] = (1, SheetMetalCut(sheet_metal_cut_width, sheet_metal_cut_height, sheet_metal_thickness))

class BendSingleDoorLeafCover(Assembly):
    def __init__(self, external_face_width:float, external_face_height:float, return_flange_width: float, sheet_metal_thickness:float):

        super().__init__()

        bend_allowance_0_deg = calculate_bend_allowance_with_radius_multiplier(bend_angle=0, thickness=sheet_metal_thickness, bend_radius_multiplier=1.5)
        
        sheet_metal_cut_width = external_face_width + 2 * return_flange_width + 2 * bend_allowance_0_deg
        sheet_metal_cut_height = external_face_height + 2 * return_flange_width + 2 * bend_allowance_0_deg

        self.components['sheet_metal_cut'] = (1, SheetMetalCut(sheet_metal_cut_width, sheet_metal_cut_height, sheet_metal_thickness))

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

DoubleRabbetProfileFrameTypes = Union[ProfileFrameDoubleRabbet, ProfileFrameDoubleRabbetWithBackbendReturn]

class DoorFrameDoubleRabbet(Assembly):
    def __init__(self, lintel: DoubleRabbetProfileFrameTypes, 
                 jamb: DoubleRabbetProfileFrameTypes,
                 grampa: Grampa):
        
        super().__init__()
        
        self.components['lintel'] = (1, lintel)
        self.components['jamb'] = (2, jamb)
        self.components['wall_plate'] = (6, WallPlate(grampa.value))

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
            self.components['intumescent_seal'] = (1, intumescent_seal)