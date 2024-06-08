# Identity Islands Visualization

## Overview

The Identity Islands Visualization application is designed to provide an interactive graphical representation of identity islands and their relationships. This application uses Dash to create a web-based interface, allowing users to explore the nodes and edges of identity islands. The nodes represent identities, and the edges represent various relationships between these identities.

## IdentityIslandsApp Class

### Initialization

The `IdentityIslandsApp` class initializes with the following components:
- **Graph Loading**: The application loads identity data from an N-Quads file into a directed graph (`DiGraph`) using NetworkX. The graph structure allows for efficient representation and manipulation of the data.
- **Layout Setup**: The positions of the nodes are determined using a spring layout algorithm, which visually separates the nodes for better readability.
- **Dash App Initialization**: The Dash application is initialized, setting up the layout and callbacks for interactive features.

### Loading Data

The `load_nquads_to_graph()` method reads the N-Quads file and populates the graph with nodes and edges. It uses regular expressions to parse lines in the file:
- **Literal Triples**: Triples with a literal object (e.g., `<subject> <predicate> "object" .`) are added as attributes to the corresponding nodes.
- **URI Triples**: Triples with a URI object (e.g., `<subject> <predicate> <object> .`) are added as edges between the subject and object nodes, with the predicate representing the edge type.

### Creating the Graph Figure

The `create_figure()` method constructs a Plotly figure to visualize the graph:
- **Edges**: The edges are represented as lines connecting the nodes, with hover information displaying the edge type.
- **Nodes**: Nodes are represented as markers, with their size and color based on their degree (number of connections). Hover information includes detailed attributes of each node.

### User Interaction and Callbacks

The `setup_layout()` method defines the layout of the Dash application, including:
- **Graph Component**: A `dcc.Graph` component displays the interactive graph.
- **Reset Button**: A button to reset the graph to its initial state.
- **Store Component**: A `dcc.Store` component to keep track of the last clicked node.

The `setup_callbacks()` method defines the interactive behavior of the application:
- **Graph Clicks**: When a node or edge is clicked, the graph updates to highlight the selected node or edge and its neighbors.
- **Reset Button**: When the reset button is clicked, the graph resets to its original state.

### Running the Application

The `run()` method starts the Dash server, making the application accessible via a web browser. The `display()` method can be used within an IPython notebook to display the application inline using an `IFrame`.

To see the visualization of the identity islands, open your web browser and go to [127.0.0.1:8050](http://127.0.0.1:8050).

### Identity Islands

The following image shows the full view of the identity islands. In total, there are 1000 islands with a 50% additional anomalies. The graph contains 11,139 nodes and 13,889 edges.

![Identity Islands](../data/identity_island_visuals/full_identity_islands.png)

### Key Features

- **Interactive Visualization**: Users can click on nodes and edges to explore their details and relationships.
- **Dynamic Highlighting**: The application highlights selected nodes and edges along with their neighbors for better context.
- **Reset Functionality**: Users can reset the graph to its initial state at any time.

### Conclusion

The Identity Islands Visualization application provides a powerful tool for exploring and understanding the complex relationships within identity islands. By leveraging Dash and NetworkX, it offers a flexible and interactive interface suitable for both development and demonstration purposes.