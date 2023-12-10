import math
import cadquery as cq


def create_wedge(radius: float, angle: float, depth: float):
    angle_rads = math.radians(90 - angle / 2)
    x_offset = radius * math.cos(angle_rads)
    y_offset = radius * math.sin(angle_rads)
    return (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(x_offset, y_offset)
        .threePointArc((0, radius), (-x_offset, y_offset))
        .close()
        .extrude(depth)
    )


def create_kemo_tweeter_fill(
    inner_diameter: float,
    outer_diameter: float,
    depth: float,
    bottom_wedge_angle: float,
):
    inner_radius = inner_diameter / 2
    outer_radius = outer_diameter / 2
    tweeter = cq.Workplane("YZ")
    cone = cq.Solid.makeCone(inner_radius, outer_radius, depth)
    tweeter.add(cone)
    wedge = create_wedge(outer_radius, bottom_wedge_angle, depth)
    tweeter = tweeter.union(wedge).rotateAboutCenter((1, 0, 0), -90)
    return tweeter


kemo_tweeter = create_kemo_tweeter_fill(
    inner_diameter=35,
    outer_diameter=41,
    depth=10,
    bottom_wedge_angle=90,
)
