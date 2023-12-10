import math
import cadquery as cq

from .params import HeadsetParams
from .kemo_tweeter import kemo_tweeter


def create_half_torus(thickness: float, radius: float):
    return (
        cq.Workplane("XZ", origin=(radius, radius, 0))
        .circle(thickness / 2)
        .revolve(180, (-radius, 0, 0), (-radius, -1, 0))
        .rotateAboutCenter((0, 1, 0), 90)
        .translate((0, -radius, 0))
    )


def create_mic_clip(
    clearance: float,
    height: float,
    protrusion: float,
    thickness: float,
):
    one_clip = (
        cq.Workplane("XY")
        .box(protrusion, thickness, height, centered=(True, True, True))
        .translate((0, (clearance + thickness) / 2, 0))
    )
    another_clip = (
        cq.Workplane("XY")
        .box(protrusion, thickness, height, centered=(True, True, True))
        .translate((0, (clearance + thickness) / -2, 0))
    )
    return one_clip.union(another_clip)


def create_headband_arc(
    radius: float,
    thickness: float,
    extension: float,
    height: float,
):
    outer_radius = radius + thickness
    wp = (
        cq.Workplane("XY")
        .moveTo(outer_radius, 0)
        .threePointArc((0, outer_radius), (-outer_radius, 0))
        .vLineTo(-extension)
        .hLineTo(-radius)
        .vLineTo(0)
        .threePointArc((0, radius), (radius, 0))
        .vLineTo(-extension)
        .hLineTo(outer_radius)
        .vLineTo(0)
        .close()
    )
    return wp.extrude(height)


def create_headband(hs: HeadsetParams):
    band = create_headband_arc(
        radius=hs.front_head.radius,
        thickness=hs.headband.thickness,
        extension=hs.headband.extension_length,
        height=hs.headband.height,
    )
    tweeter_z = kemo_tweeter.val().Center().z
    headband_z = band.val().Center().z
    # Add tweeters to the front
    for angle in hs.headband.tweeter_positions:
        tweeter_radius = hs.front_head.radius + hs.headband.tweeter_indent
        tweeter_x = tweeter_radius * math.cos(math.radians(90 + angle))
        tweeter_y = tweeter_radius * math.sin(math.radians(90 + angle))
        tweeter = kemo_tweeter.translate(
            (
                tweeter_x,
                tweeter_y,
                headband_z - tweeter_z,
            )
        ).rotateAboutCenter((0, 0, 1), angle)
        band = band.cut(tweeter)
    # Add mic clips to the sides
    mic_clip = create_mic_clip(
        clearance=hs.headband.mic_clip_clearance,
        height=hs.headband.mic_clip_height,
        protrusion=hs.headband.mic_clip_protrusion,
        thickness=hs.headband.mic_clip_thickness,
    )
    left_face = band.faces("<X").val()
    right_face = band.faces(">X").val()
    left_clip = mic_clip.translate(left_face.Center()).translate(
        (-hs.headband.mic_clip_protrusion / 2, 0, 0)
    )
    right_clip = mic_clip.translate(right_face.Center()).translate(
        (hs.headband.mic_clip_protrusion / 2, 0, 0)
    )
    band = band.union(left_clip).union(right_clip)
    # Add loops to the back
    loop = create_half_torus(
        hs.headband.attachment_thickness,
        hs.headband.attachment_radius,
    )
    for face in band.faces("<Y").vals():
        face_loop = loop.translate(face.Center())
        band = band.union(face_loop)
    return band
