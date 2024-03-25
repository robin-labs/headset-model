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
    # Positions of  Kemo tweeters (degrees relative to 0˚ = front)
    tweeter_positions: list[float]
    # How far forward to push the tweeters in the headband
    tweeter_indent: float
    # Microphone clip height
    mic_clip_height: float
    # Microphone clip clearance (~width of mic board)
    mic_clip_clearance: float
    # Microphone clip protrusion from side
    mic_clip_protrusion: float
    # Microphone clip thickness
    mic_clip_thickness: float


@dataclass
class HeadboxParams:
    # The depth of the headbox
    depth: float
    # The thickness of the control board holder
    wall_thickness: float
    # The peneration of the head into the headbox
    head_penetration: float
    # The cutout cylinder penetration
    deep_cutout_penetration: float
    # The radius of the cutout cylinder
    deep_cutout_radius: float
    # The strap cutout width
    strap_cutout_width: float
    # The strap cutout height
    strap_cutout_height: float
    # The strap cutout depth
    strap_cutout_depth: float


@dataclass
class ControlBoardParams:
    # The width of the control board
    width: float
    # The height of the control board
    height: float
    # The depth of the control board
    depth: float


@dataclass
class BatteryParams:
    # The width of the battery
    width: float
    # The height of the battery
    height: float
    # The depth of the battery
    depth: float


@dataclass
class HeadsetParams:
    front_head: HeadParams
    back_head: HeadParams
    headband: HeadbandParams
    headbox: HeadboxParams
    battery: BatteryParams
    control_board: ControlBoardParams
