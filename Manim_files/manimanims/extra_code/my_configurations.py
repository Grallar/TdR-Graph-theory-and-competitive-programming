from manim import config

label_colour = config.background_color

vertex_configuration = {"color": config.background_color.invert()}
edge_configuration = {"color": config.background_color.invert()}

graph_configuration = {
    "labels": True,
    "layout_scale": 2,
    "layout": "circular",
    "label_fill_color": label_colour,
    "vertex_config": vertex_configuration,
    "edge_config": edge_configuration,
}
