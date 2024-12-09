from attributes import Sentido, Marco, Grampa
from base_classes import Hinge, SingleDoor, SingleDoorLeaf, DoorFrameDoubleRabbet, BendSingleDoorLeafBase, BendSingleDoorLeafCover, Core, ProfileFrameDoubleRabbet, ProfileFrameDoubleRabbetWithBackbendReturn
from specific_parts import FireproofPanel, LiteHingeRight, LiteHingeLeft, IntumescentSeal10x1
from typing import Union

class LiteProfileFrameDoubleRabbet100(ProfileFrameDoubleRabbetWithBackbendReturn):
    SHEET_METAL_THICKNESS = 1.2
    FRAME_RABBET_FOR_LEAF = 52
    FRAME_BACKBEND_RETURN = 10
    FRAME_BACKBEND = 10
    FRAME_FACE = 50
    FRAME_STOP = 20
    FRAME_SOFFIT = 20
    FRAME_RABBET_FIXED = 20

    def __init__(self, length: float):
        super().__init__(
            length=length,
            frame_backbend_return=self.FRAME_BACKBEND_RETURN,
            frame_backbend=self.FRAME_BACKBEND,
            frame_face=self.FRAME_FACE,
            frame_stop=self.FRAME_STOP,
            frame_soffit=self.FRAME_SOFFIT,
            frame_rabbet_fixed=self.FRAME_RABBET_FIXED,
            frame_rabbet_for_leaf=self.FRAME_RABBET_FOR_LEAF,
            sheet_metal_thickness=self.SHEET_METAL_THICKNESS
        )

class LiteProfileFrameDoubleRabbet120(ProfileFrameDoubleRabbet):
    SHEET_METAL_THICKNESS = 1.2
    FRAME_RABBET_FOR_LEAF = 52
    FRAME_BACKBEND = 10
    FRAME_FACE = 50
    FRAME_STOP = 20
    FRAME_SOFFIT = 20
    FRAME_RABBET_FIXED = 20

    def __init__(self, length: float):
        super().__init__(
            length=length,
            frame_backbend=self.FRAME_BACKBEND,
            frame_face=self.FRAME_FACE,
            frame_stop=self.FRAME_STOP,
            frame_soffit=self.FRAME_SOFFIT,
            frame_rabbet_fixed=self.FRAME_RABBET_FIXED,
            frame_rabbet_for_leaf=self.FRAME_RABBET_FOR_LEAF,
            sheet_metal_thickness=self.SHEET_METAL_THICKNESS
        )

class LiteProfileFrameDoubleRabbet140(ProfileFrameDoubleRabbet):
    SHEET_METAL_THICKNESS = 1.2
    FRAME_RABBET_FOR_LEAF = 52
    FRAME_BACKBEND = 10
    FRAME_FACE = 50
    FRAME_STOP = 20
    FRAME_SOFFIT = 20
    FRAME_RABBET_FIXED = 20

    def __init__(self, length: float):
        super().__init__(
            length=length,
            frame_backbend=self.FRAME_BACKBEND,
            frame_face=self.FRAME_FACE,
            frame_stop=self.FRAME_STOP,
            frame_soffit=self.FRAME_SOFFIT,
            frame_rabbet_fixed=self.FRAME_RABBET_FIXED,
            frame_rabbet_for_leaf=self.FRAME_RABBET_FOR_LEAF,
            sheet_metal_thickness=self.SHEET_METAL_THICKNESS
        )

class LiteBendSingleDoorLeafBase(BendSingleDoorLeafBase):
    
    INTERIOR_DEPTH = 50
    ASSEMBLY_FLANGE_WIDTH = 5
    SHEET_METAL_THICKNESS = 0.9
    
    def __init__(self, external_width_body: float, external_height_body: float):
        super().__init__(
            external_width_body=external_width_body,
            external_height_body=external_height_body,
            internal_depth=self.INTERIOR_DEPTH,
            assembly_flange_width=self.ASSEMBLY_FLANGE_WIDTH,
            sheet_metal_thickness=self.SHEET_METAL_THICKNESS
        )

class LiteBendSingleDoorLeafCover(BendSingleDoorLeafCover):
   RETURN_FLANGE_WIDTH = 5 
   SHEET_METAL_THICKNESS = 0.9
   FACE_OVERLAP = 18

   def __init__(self, external_face_width: float, external_face_height: float):
       super().__init__(
           external_face_width=external_face_width,
           external_face_height=external_face_height,
           return_flange_width=self.RETURN_FLANGE_WIDTH,
           sheet_metal_thickness=self.SHEET_METAL_THICKNESS
       )



class LiteSingleDoorLeaf(SingleDoorLeaf):
   FACE_OVERLAP = 9

   def __init__(self, external_width_body: float, external_height_body: float):
       base = LiteBendSingleDoorLeafBase(
           external_width_body=external_width_body,
           external_height_body=external_height_body
       )

       cover = LiteBendSingleDoorLeafCover(
           external_face_width=external_width_body + self.FACE_OVERLAP * 2,
           external_face_height=external_height_body + self.FACE_OVERLAP * 2
       )

       core = FireproofPanel()

       super().__init__(base, cover, core)

DoubleRabbetProfileFrameTypes = Union[ProfileFrameDoubleRabbet, ProfileFrameDoubleRabbetWithBackbendReturn]

class LiteDoorFrameDoubleRabbet(DoorFrameDoubleRabbet):
    def __init__(self, lintel: DoubleRabbetProfileFrameTypes, jamb: DoubleRabbetProfileFrameTypes, grampa: Grampa):
        
        super().__init__(
            lintel=lintel,
            jamb=jamb, 
            grampa=grampa
        )

class LiteSingleDoor(SingleDoor):
    def __init__(self, ancho_pl: int, alto_pl: int, sentido: Sentido, 
                 marco: Marco, grampa: Grampa):
        
        door_leaf = LiteSingleDoorLeaf(
            external_width_body=ancho_pl,
            external_height_body=alto_pl
        )

        door_frame = LiteDoorFrameDoubleRabbet(
            lintel=self.get_frame_profile_for_frame(marco, ancho_pl + 100),
            jamb=self.get_frame_profile_for_frame(marco, alto_pl + 50), 
            grampa=grampa
        )

        intumescent_seal = IntumescentSeal10x1()

        super().__init__(
            door_leaf=door_leaf,
            door_frame=door_frame,
            hinges=(3, self.get_hinge_from_sentido(sentido)),
            intumescent_seal=intumescent_seal
        )

    def get_hinge_from_sentido(self, sentido: Sentido) -> Hinge:
        if sentido == Sentido.IZQUIERDA:
            return LiteHingeLeft()
        else:
            return LiteHingeRight()

    def get_frame_profile_for_frame(self, marco: Marco, length: float) -> DoubleRabbetProfileFrameTypes:
        if marco == Marco.INT_100_EXT_130:
            return LiteProfileFrameDoubleRabbet100(length=length)
        elif marco == Marco.INT_120_EXT_150:
            return LiteProfileFrameDoubleRabbet120(length=length)
        else:
            return LiteProfileFrameDoubleRabbet140(length=length)


if __name__ == "__main__":
    puerta_simple_lite_900_2000 = LiteSingleDoor(900, 2000, Sentido.IZQUIERDA, Marco.INT_100_EXT_130, Grampa.DURLOCK)
    puerta_simple_lite_900_2000.show_components()