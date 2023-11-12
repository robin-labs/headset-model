import cadquery as cq

from .params import HeadsetParams


def create_strap_guide(
    height: float,
    width: float,
    depth: float,
    strap_clearance: float,
):
    padding = depth - strap_clearance
    assert padding >= 0.1
    outer_rect = (
        cq.Workplane("YZ")
        .rect(
            strap_clearance + padding * 2, height + padding * 2, centered=(True, True)
        )
        .extrude(width)
    )
    inner_rect = (
        cq.Workplane("YZ")
        .rect(strap_clearance + padding * 2, height, centered=(True, True))
        .extrude(width)
        .translate((0, padding, 0))
    )
    y_offset = outer_rect.faces(">Y").val().Center().y
    return outer_rect.cut(inner_rect).translate((0, -y_offset, 0))


def create_headbox_arc(
    width: float,
    height: float,
    head_radius: float,
    head_radius_penetration: float,
):
    arc_box = cq.Workplane("XZ").box(
        width,
        height,
        head_radius_penetration,
        centered=(True, True, False),
    )
    arc_cyclinder = (
        cq.Workplane("XY", origin=(0, head_radius - head_radius_penetration))
        .circle(head_radius)
        .extrude(height, both=True)
    )
    y_depth = arc_box.faces("<Y").val().Center().y
    return arc_box.cut(arc_cyclinder).translate((0, -y_depth))


def create_cutout_cylinder(
    radius: float,
    height: float,
    penetration: float,
):
    return (
        cq.Workplane("XY", origin=(0, radius - penetration))
        .circle(radius)
        .extrude(height / 2, both=True)
    )


def create_screw_mount(
    hole_diameter: float,
    hole_padding: float,
    depth: float,
):
    inner_radius = hole_diameter / 2
    outer_radius = inner_radius + hole_padding
    outer_cylinder = cq.Workplane("XZ").circle(outer_radius).extrude(depth)
    inner_cylinder = cq.Workplane("XZ").circle(inner_radius).extrude(depth)
    return outer_cylinder.cut(inner_cylinder)


def create_headbox(hs: HeadsetParams):
    arc = create_headbox_arc(
        width=hs.headbox.width,
        height=hs.headbox.height,
        head_radius=hs.head.radius,
        head_radius_penetration=hs.headbox.head_penetration,
    )
    box = cq.Workplane("XZ").box(
        hs.headbox.width,
        hs.headbox.height,
        hs.headbox.depth,
        centered=(True, True, False),
    )
    cutout_cylinder = create_cutout_cylinder(
        radius=hs.headbox.deep_cutout_radius,
        height=hs.headbox.strap_cutout_height,
        penetration=hs.headbox.deep_cutout_penetration,
    )
    box = box.union(arc).cut(cutout_cylinder)
    through_hole = (
        cq.Workplane("XZ")
        .box(
            2 * hs.headbox.strap_clearance,
            hs.headbox.strap_cutout_height,
            hs.headbox.depth * 2,
            centered=(True, True, False),
        )
        .edges("|Y")
        .fillet(0.1)
    )
    box = box.cut(through_hole)
    for strap_position in (
        -hs.headbox.width / 2,
        hs.headbox.width / 2 - hs.headbox.strap_guide_width,
    ):
        strap_guide = create_strap_guide(
            height=hs.headbox.strap_cutout_height,
            width=hs.headbox.strap_guide_width,
            depth=hs.headbox.strap_guide_depth,
            strap_clearance=hs.headbox.strap_clearance,
        ).translate((strap_position, -hs.headbox.depth, 0))
        box = box.union(strap_guide)
    # Add holes for the control board
    spacing_x, spacing_z = (
        hs.control_board.screw_spacing_x,
        hs.control_board.screw_spacing_z,
    )
    board_hole_positions = [
        (spacing_x / 2, spacing_z / 2),
        (-spacing_x / 2, spacing_z / 2),
        (-spacing_x / 2, -spacing_z / 2),
        (spacing_x / 2, -spacing_z / 2),
    ]
    for x, z in board_hole_positions:
        box = box.union(
            create_screw_mount(
                hole_diameter=hs.control_board.screw_hole_diameter,
                hole_padding=hs.control_board.screw_mount_padding,
                depth=hs.control_board.screw_mount_clearance,
            ).translate((x, 0, z))
        )
    return box
