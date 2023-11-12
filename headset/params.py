from dataclasses import dataclass
import math


@dataclass
class HeadParams:
    circumference: float

    @property
    def diameter(self):
        return self.circumference / math.pi

    @property
    def radius(self):
        return self.diameter / 2


@dataclass
class HeadbandParams:
    # The thickness of the headband
    thickness: float
    # The height of the headband
    height: float
    # The length the headband extends past the arc
    # As this increases it takes on a horseshoe shape
    extension_length: float
    # The radius of the attachment loops
    attachment_radius: float
    # The thickness of the attachment loops
    attachment_thickness: float


@dataclass
class HeadboxParams:
    # The width of the headbox
    width: float
    # The height of the headbox
    height: float
    # The depth of the headbox
    depth: float
    # The peneration of the head into the headbox
    head_penetration: float
    # The cutout cylinder penetration
    deep_cutout_penetration: float
    # The radius of the cutout cylinder
    deep_cutout_radius: float
    # The strap cutout height
    strap_cutout_height: float
    # The strap clearance
    strap_clearance: float
    # The strap guide depth
    strap_guide_depth: float
    # The strap guide width
    strap_guide_width: float


@dataclass
class ControlBoardParams:
    # The x-axis screw spacing
    screw_spacing_x: float
    # The z-axis screw spacing
    screw_spacing_z: float
    # The screw diameter
    screw_hole_diameter: float
    # The screw mount padding
    screw_mount_padding: float
    # The clearance above the headbox
    screw_mount_clearance: float


@dataclass
class HeadsetParams:
    head: HeadParams
    headband: HeadbandParams
    headbox: HeadboxParams
    control_board: ControlBoardParams
