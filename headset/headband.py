import cadquery as cq

from .params import HeadsetParams


def create_half_torus(thickness: float, radius: float):
    return (
        cq.Workplane("XZ", origin=(radius, radius, 0))
        .circle(thickness / 2)
        .revolve(180, (-radius, 0, 0), (-radius, -1, 0))
        .rotateAboutCenter((0, 1, 0), 90)
        .translate((0, -radius, 0))
    )


def create_headband_arc(
    radius: float,
    thickness: float,
    extension: float,
    height: float,
):
    inner_radius = radius - thickness
    wp = (
        cq.Workplane("XY")
        .moveTo(radius, 0)
        .threePointArc((0, radius), (-radius, 0))
        .vLineTo(-extension)
        .hLineTo(-inner_radius)
        .vLineTo(0)
        .threePointArc((0, inner_radius), (inner_radius, 0))
        .vLineTo(-extension)
        .hLineTo(radius)
        .vLineTo(0)
        .close()
    )
    return wp.extrude(height)


def create_headband(hs: HeadsetParams):
    band = create_headband_arc(
        radius=hs.head.radius,
        thickness=hs.headband.thickness,
        extension=hs.headband.extension_length,
        height=hs.headband.height,
    )
    loop = create_half_torus(0.3, 1)
    for face in band.faces("<Y").vals():
        face_loop = loop.translate(face.Center())
        band = band.union(face_loop)
    return band
