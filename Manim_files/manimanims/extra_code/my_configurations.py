from manim import config
from manim.mobject.geometry.arc import LabeledDot
from manim.mobject.geometry.line import Line


labels = True
label_fill_colour = config.background_color
layout = "circular"
layout_scale = 2
vertex_config = {"color": config.background_color.invert()}
edge_config = {"color": config.background_color.invert()}
layout_config = None
vertex_type = LabeledDot
vertex_mobjects = None
edge_type = Line
partitions = None
root_vertex = None

graph_configuration = {
    "labels": labels,
    "label_fill_color": label_fill_colour,
    "layout": layout,
    "layout_scale": 2,
    "vertex_config": vertex_config,
    "edge_config": edge_config,
    "layout_config": layout_config,
    "vertex_type": vertex_type,
    "vertex_mobjects": vertex_mobjects,
    "edge_type": edge_type,
    "partitions": partitions,
    "root_vertex": root_vertex,
}
