import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, ColumnDataSource, Label, LabelSet
from bokeh.palettes import Spectral8
from graph import Graph


class BokehGraph:
    def __init__(self, graph):
        self.graph = graph
    def draw(self):
        graph = self.graph

        N = len(graph.vertices)
        node_indices = list(graph.vertices)

        plot = figure(title='Graph Layout Demonstration', x_range=(-1.1,12.1), y_range=(-1.1,12.1),
                    tools='', toolbar_location=None)

        graph_renderer = GraphRenderer()

        graph_renderer.node_renderer.data_source.add(node_indices, 'index')
        graph_renderer.node_renderer.data_source.add([graph.vertices[vertex_id].color for vertex_id in graph.vertices], 'color')
        graph_renderer.node_renderer.glyph = Circle(radius=0.5, fill_color='color')

        start_indices = []
        end_indices = []

        for vertex in graph.vertices:
            for edge_end in graph.vertices[vertex].edges:
                start_indices.append(vertex)
                end_indices.append(edge_end)
        # print(start_indices)
        # print(end_indices)


        graph_renderer.edge_renderer.data_source.data = dict(
            start=start_indices,
            end=end_indices)

        ### start of layout code
        
        x = [graph.vertices[vertex_id].x for vertex_id in graph.vertices]
        y = [graph.vertices[vertex_id].y for vertex_id in graph.vertices]
        # x = [i for i in grid]
        # y = [i ** 2 for i in grid]

        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph_renderer)

        labelSource = ColumnDataSource(data=dict(x=x, y=y, names=[graph.vertices[vertex_id].id for vertex_id in graph.vertices]))
        labels = LabelSet(x='x', y='y', text='names', level='glyph',
                    text_align='center', text_baseline='middle', source=labelSource, render_mode='canvas')


        plot.add_layout(labels)


        output_file('graph.html')
        show(plot)