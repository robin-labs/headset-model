import cadquery as cq

from .params import HeadsetParams


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


def create_battery_holder(
    battery_width: float,
    battery_height: float,
    battery_depth: float,
    container_width: float,
    container_height: float,
):
    outer_box = cq.Workplane("XZ").box(
        container_width,
        container_height,
        battery_depth,
        centered=(True, True, False),
    )
    inner_box = cq.Workplane("XZ").box(
        battery_width,
        battery_height,
        battery_depth,
        centered=(True, True, False),
    )
    return outer_box.cut(inner_box)


def create_control_board_holder(
    control_board_width: float,
    control_board_height: float,
    control_board_depth: float,
    container_width: float,
    container_height: float,
    wall_thickness: float,
    ethernet_cutout_width: float = 20,
):
    outer_box = cq.Workplane("XZ").box(
        container_width,
        container_height,
        control_board_depth + wall_thickness,
        centered=(True, True, False),
    )

    inner_box = (
        cq.Workplane("XZ")
        .box(
            control_board_width,
            control_board_height + 2 * wall_thickness,
            control_board_depth,
            centered=(True, True, False),
        )
        .translate((0, 0, wall_thickness))
    )
    ethernet_x = (control_board_width - ethernet_cutout_width) / 2
    ethernet_z = -(control_board_height - ethernet_cutout_width) / 2 - wall_thickness
    ethernet_cutout = (
        cq.Workplane("XZ")
        .box(
            ethernet_cutout_width,
            ethernet_cutout_width,
            control_board_depth,
            centered=(True, True, False),
        )
        .translate((ethernet_x, 0, ethernet_z))
    )
    return outer_box.cut(inner_box).cut(ethernet_cutout)


def bind_to_top_surface(box: cq.Workplane, target: cq.Workplane, cut: bool = False):
    box_y_extent = box.faces("<Y").val().Center().y
    target_y_extent = target.faces("<Y" if cut else ">Y").val().Center().y
    target = target.translate((0, box_y_extent - target_y_extent, 0))
    if cut:
        return box.cut(target)
    else:
        return box.union(target)


def create_headbox(hs: HeadsetParams):
    headbox_height = 2 * hs.headbox.wall_thickness + hs.control_board.height
    headbox_width = 2 * hs.headbox.wall_thickness + hs.control_board.width
    arc = create_headbox_arc(
        width=headbox_width,
        height=headbox_height,
        head_radius=hs.back_head.radius,
        head_radius_penetration=hs.headbox.head_penetration,
    )
    box = cq.Workplane("XZ").box(
        headbox_width,
        headbox_height,
        hs.headbox.depth,
        centered=(True, True, False),
    )
    cutout_cylinder = create_cutout_cylinder(
        radius=hs.headbox.deep_cutout_radius,
        height=3 * hs.headbox.strap_cutout_height,
        penetration=hs.headbox.deep_cutout_penetration,
    )
    box = box.union(arc).cut(cutout_cylinder)
    box = bind_to_top_surface(
        box=box,
        target=cq.Workplane("XZ").box(
            headbox_width,
            hs.headbox.strap_cutout_height,
            hs.headbox.strap_cutout_depth,
            centered=(True, True, True),
        ),
        cut=True,
    )
    box = bind_to_top_surface(
        box=box,
        target=create_battery_holder(
            battery_width=hs.battery.width,
            battery_height=hs.battery.height,
            battery_depth=hs.battery.depth,
            container_width=headbox_width,
            container_height=headbox_height,
        ),
    )
    box = bind_to_top_surface(
        box=box,
        target=create_control_board_holder(
            control_board_width=hs.control_board.width,
            control_board_height=hs.control_board.height,
            control_board_depth=hs.control_board.depth,
            container_width=headbox_width,
            container_height=headbox_height,
            wall_thickness=hs.headbox.wall_thickness,
        ),
    )
    return box
