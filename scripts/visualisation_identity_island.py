import networkx as nx
import re
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from IPython.display import IFrame

class IdentityIslandsApp:
    def __init__(self, nquads_file, base_uri="http://syntetic_identity_island.org/"):
        self.G = self.load_nquads_to_graph(nquads_file, base_uri)
        self.pos = nx.spring_layout(self.G)
        nx.set_node_attributes(self.G, self.pos, 'pos')
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def load_nquads_to_graph(self, nquads_file, base_uri):
        G = nx.DiGraph()
        pattern_literal = re.compile(r'<(.*?)>\s+<(.*?)>\s+"(.*?)"\s*(?:\^\^<.*?>)?\s*\.\s*')
        pattern_uri = re.compile(r'<(.*?)>\s+<(.*?)>\s+<(.*?)>\s*\.\s*')
        
        with open(nquads_file, 'r') as f:
            for line in f:
                match_literal = pattern_literal.match(line)
                match_uri = pattern_uri.match(line)
                if match_literal:
                    subject = match_literal.group(1)
                    predicate = match_literal.group(2)
                    obj = match_literal.group(3)
                    
                    if predicate.startswith(base_uri):
                        pred_key = predicate[len(base_uri):]

                        # Ensure the subject node exists
                        if subject not in G:
                            G.add_node(subject)
                        
                        # Add attributes to the node
                        if pred_key not in G.nodes[subject]:
                            G.nodes[subject][pred_key] = obj
                        else:
                            if isinstance(G.nodes[subject][pred_key], list):
                                G.nodes[subject][pred_key].append(obj)
                            else:
                                G.nodes[subject][pred_key] = [G.nodes[subject][pred_key], obj]
                
                elif match_uri:
                    subject = match_uri.group(1)
                    predicate = match_uri.group(2)
                    obj = match_uri.group(3)
                    
                    if predicate.startswith(base_uri):
                        pred_key = predicate[len(base_uri):]

                        # Ensure the subject node exists
                        if subject not in G:
                            G.add_node(subject)
                        # Ensure the object node exists if it's also a subject
                        if obj not in G:
                            G.add_node(obj)
                        
                        # Add an edge
                        G.add_edge(subject, obj, type=pred_key)
        
        return G

    def create_figure(self, highlight_nodes=None):
        edge_trace = []
        hover_edge_trace = []

        nodes_to_highlight = set()
        
        if highlight_nodes is not None:
            nodes_to_highlight.update(highlight_nodes)
            for node in highlight_nodes:
                nodes_to_highlight.update(set(self.G.neighbors(node)))

        for edge in self.G.edges(data=True):
            if highlight_nodes is None or (edge[0] in nodes_to_highlight and edge[1] in nodes_to_highlight):
                x0, y0 = self.pos[edge[0]]
                x1, y1 = self.pos[edge[1]]
                edge_info = f"Edge: {edge[0]}-{edge[1]}<br>Type: {edge[2].get('type', 'N/A')}"
        
                edge_trace.append(
                    go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        line=dict(width=1, color='#888'),
                        mode='lines',
                        hoverinfo='none',
                        visible=True
                    )
                )
        
                hover_edge_trace.append(
                    go.Scatter(
                        x=[(x0 + x1) / 2],
                        y=[(y0 + y1) / 2],
                        mode='markers',
                        marker=dict(size=0.5, color='#888'),
                        hoverinfo='text',
                        text=[f"Type: {edge[2].get('type', 'N/A')}"],
                        hovertemplate='%{text}<extra></extra>',
                        visible=True
                    )
                )

        node_x = []
        node_y = []
        node_color = []
        node_size = []
        node_text = []

        for node in self.G.nodes(data=True):
            if highlight_nodes is None or node[0] in nodes_to_highlight:
                x, y = self.pos[node[0]]
                node_x.append(x)
                node_y.append(y)
                degree = nx.degree(self.G, node[0])
                num_neighbors = len(list(self.G.neighbors(node[0])))

                node_color.append(degree)
                node_size.append(10 + 2 * degree)

                attributes = node[1] if isinstance(node[1], dict) else {}
                attr_text = '<br>'.join([f"{key}: {value}" for key, value in attributes.items()])
                node_text.append(f"ID: {node[0]}<br>degree: {degree}<br>neighbors: {num_neighbors}<br>{attr_text}")

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            text=node_text,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis_r',
                color=node_color,
                size=node_size,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        )

        fig = go.Figure(data=edge_trace + hover_edge_trace + [node_trace],
                        layout=go.Layout(
                            title='Identity Islands',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))

        fig.update_layout(width=1800, height=1000)
        return fig

    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Graph(id='network-graph', figure=self.create_figure(), style={'width': '100%', 'height': '90vh'}),
            html.Button('Reset', id='reset-button', n_clicks=0, style={'position': 'absolute', 'top': '10px', 'right': '240px'}),
            dcc.Store(id='last-clicked-node', data=None)
        ])

    def setup_callbacks(self):
        @self.app.callback(
            [Output('network-graph', 'figure'),
             Output('last-clicked-node', 'data')],
            [Input('network-graph', 'clickData'),
             Input('reset-button', 'n_clicks')],
            [State('last-clicked-node', 'data')]
        )
        def update_figure(clickData, resetClicks, last_clicked_node):
            ctx = dash.callback_context

            if not ctx.triggered:
                return self.create_figure(), None

            trigger = ctx.triggered[0]['prop_id']

            if 'reset-button' in trigger:
                return self.create_figure(), None

            if clickData is not None:
                text = clickData['points'][0]['text']
                if 'Type:' in text:
                    edge_info = text.split('<br>')[0].split(': ')[1]
                    for edge in self.G.edges(data=True):
                        edge_type = f"Type: {edge[2].get('type', 'N/A')}"
                        if edge_type == text:
                            edge = (edge[0], edge[1])
                            return self.create_figure(highlight_nodes=[edge[0], edge[1]]), last_clicked_node
                else:
                    node_id = text.split('<br>')[0].split(': ')[1]
                    return self.create_figure(highlight_nodes=[node_id]), node_id

            return self.create_figure(), None

    def run(self):
        self.app.run_server(debug=True)

    def display(self):
        return IFrame(src="http://127.0.0.1:8050", width='100%', height='1000px')


if __name__ == '__main__':
    app_instance = IdentityIslandsApp('./data/ingested_data/syntetic_identity_island.nq')
    app_instance.run()