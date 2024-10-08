from nodes import *
from typing import Dict
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random


# def csv_to_nodes(bg_csv, pf_csv, po_csv, m_csv, p_csv):
#     import pandas as pd
#
#     bg_df = pd.read_csv(bg_csv)
#     for _, i in bg_df.iterrows():
#



def query_subgraph(
    G_d: nx.Graph,
    node_id: str,
    levels: int = 2,
    target_node_id: str = None,
    highlight_shortest_path: bool = False,
):
    G = G_d.to_undirected()
    if node_id not in G.nodes:
        raise ValueError(f"Node {node_id} does not exist in the graph.")

    subgraph_nodes = {node_id}
    current_level_nodes = {node_id}

    for _ in range(levels):
        next_level_nodes = set()
        for node in current_level_nodes:
            next_level_nodes.update(G.neighbors(node))
        subgraph_nodes.update(next_level_nodes)
        current_level_nodes = next_level_nodes

    subgraph = G.subgraph(subgraph_nodes)
    # print("Subgraph nodes:", subgraph_nodes)
    pos = nx.spring_layout(subgraph, k=0.5, iterations=50)

    edge_x, edge_y = [], []
    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x, node_y = [], []
    for node in subgraph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(subgraph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(
            f"{subgraph.nodes[adjacencies[0]]['id']} - {subgraph.nodes[adjacencies[0]]['name']} <br># of connections: {len(adjacencies[1])}"
        )

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig_data = [edge_trace, node_trace]

    if highlight_shortest_path and target_node_id:
        if target_node_id not in G.nodes:
            raise ValueError(
                f"Target node {target_node_id} does not exist in the graph."
            )

        try:
            shortest_path = nx.shortest_path(G, source=node_id, target=target_node_id)
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            path_edge_x, path_edge_y = [], []
            for edge in path_edges:
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                path_edge_x.extend([x0, x1, None])
                path_edge_y.extend([y0, y1, None])

            path_edge_trace = go.Scatter(
                x=path_edge_x,
                y=path_edge_y,
                line=dict(width=2, color="red"),
                hoverinfo="none",
                mode="lines",
            )

            path_node_x, path_node_y = [], []
            for node in shortest_path:
                x, y = pos[node]
                path_node_x.append(x)
                path_node_y.append(y)

            path_node_trace = go.Scatter(
                x=path_node_x,
                y=path_node_y,
                mode="markers",
                hoverinfo="text",
                marker=dict(color="red", size=12, line_width=2),
            )

            fig_data.extend([path_edge_trace, path_node_trace])
            title = f"Subgraph for node: {node_id} (Levels: {levels}) with Shortest Path to {target_node_id}"
        except nx.NetworkXNoPath:
            title = f"Subgraph for node: {node_id} (Levels: {levels}) - No Path to {target_node_id}"
    else:
        title = f"Subgraph for node: {node_id} (Levels: {levels})"

    fig = go.Figure(
        data=fig_data,
        layout=go.Layout(
            title=title,
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    fig.show()


class GraphData:
    def __init__(self):
        self.business_groups: Dict[str, BusinessGroup] = {}
        self.product_families: Dict[str, ProductFamily] = {}
        self.product_offerings: Dict[str, ProductOffering] = {}
        self.modules: Dict[str, Modules] = {}
        self.parts: Dict[str, Parts] = {}
        self.COLOR_MAP = {
            "BusinessGroup": "#FF9999",
            "ProductFamily": "#66B2FF",
            "ProductOffering": "#99FF99",
            "module": "#FFCC99",
            "make": "#FF99CC",
            "purchase": "#99CCFF",
        }

    def visualize_graph_nx(self, G: nx.DiGraph):
        pos = nx.spring_layout(G, k=1, iterations=50)
        for type in self.COLOR_MAP:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[
                    node for node, data in G.nodes(data=True) if data["type"] == type
                ],
                node_color=self.COLOR_MAP[type],
                node_size=250,
                alpha=0.8,
                label=type,
            )
            nx.draw_networkx_labels(
                G,
                pos,
                font_size=8,
                font_color="black",
                labels={
                    node: data["id"]
                    for node, data in G.nodes(data=True)
                    if data["type"] == type
                },
            )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=G.edges(),
            width=1.0,
            alpha=0.8,
            edge_color="black",
        )
        plt.show()

    def visualize_graph_plotly(self, G: nx.DiGraph):
        pos = nx.spring_layout(G, k=1, iterations=10)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                showscale=True,
                colorscale="YlGnBu",
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

        # Add node attributes
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                f"{G.nodes[adjacencies[0]]['id']} - {G.nodes[adjacencies[0]]['name']} <br># of connections: {len(adjacencies[1])}"
            )

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        # Create the figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title="Network Graph Visualization",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.005,
                        y=-0.002,
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        fig.show()

    def add_business_group(self, business_group: BusinessGroup):
        self.business_groups[business_group.id] = business_group

    def add_product_family(self, product_family: ProductFamily):
        self.product_families[product_family.id] = product_family

    def add_product_offering(self, product_offering: ProductOffering):
        self.product_offerings[product_offering.id] = product_offering

    def add_modules(self, module: Modules):
        self.modules[module.id] = module

    def add_parts(self, part: Parts):
        self.parts[part.id] = part

    def create_graph(self):
        G = nx.DiGraph()
        for business_group in self.business_groups.values():
            G.add_node(
                business_group.id,
                id=business_group.id,
                name=business_group.name,
                type="BusinessGroup",
                revenue=business_group.revenue,
                time_stamp=business_group.time_stamp,
            )
        for product_family in self.product_families.values():
            G.add_node(
                product_family.id,
                id=product_family.id,
                name=product_family.name,
                type="ProductFamily",
                business_group_id=product_family.business_group_id,
                time_stamp=product_family.time_stamp,
            )
        for product_offering in self.product_offerings.values():
            G.add_node(
                product_offering.id,
                id=product_offering.id,
                name=product_offering.name,
                type="ProductOffering",
                product_family_id=product_offering.product_family_id,
                inventory=product_offering.inventory,
            )

        for module in self.modules.values():
            G.add_node(
                module.id,
                id=module.id,
                name=module.name,
                type="module",
                product_offering_id=module.product_offering_id,
                inventory=module.inventory,
                importance=module.importance,
            )

        for offering in self.product_offerings.values():
            G.add_edge(offering.id, offering.product_family_id)

        for family in self.product_families.values():
            G.add_edge(family.id, family.business_group_id)

        for module in self.modules.values():
            for offering in module.product_offering_id:
                G.add_edge(module.id, offering)

        return G

    def random_node_generator(self, node_type: str, num: int, max_connections: int = 5):
        if node_type.lower() == "module":
            for i in range(num):
                j = random.randint(1, max_connections)
                product_offering_ids = []
                for k in range(j):
                    product_offering_ids.append(
                        random.choice(list(self.product_offerings.keys()))
                    )
                module = Modules(
                    id=f"M_{i}",
                    name=f"Module_{i}",
                    product_offering_id=product_offering_ids,
                )
                self.add_modules(module)

        elif node_type.lower() == "part":
            for i in range(num):
                j = random.randint(1, max_connections)
                module_ids = []
                for k in range(j):
                    module_ids.append(random.choice(list(self.modules.keys())))
                part = Parts(
                    id=f"P_{i}",
                    name=f"Part_{i}",
                    module_id=module_ids,
                )
                self.add_parts(part)

    def nodes_to_csv(self):
        import csv, os, pandas as pd
        os.makedirs("data", exist_ok=True)
        file_names = {
            "BusinessGroup": "data/business_groups.csv",
            "ProductFamily": "data/product_families.csv",
            "ProductOffering": "data/product_offerings.csv",
            "Modules": "data/modules.csv",
            "Parts": "data/parts.csv",
        }
        edges_list = []

        with open(file_names["BusinessGroup"], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "revenue", "time_stamp"])
            for bg in self.business_groups.values():
                writer.writerow([bg.id, bg.name, bg.revenue, bg.time_stamp])

        with open(file_names["ProductFamily"], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "time_stamp"])
            for pf in self.product_families.values():
                writer.writerow([pf.id, pf.name, pf.time_stamp])
                edges_list.append({"source": pf.id, "target": pf.business_group_id})


        with open(file_names["ProductOffering"], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "inventory", "demand", "time_stamp"])
            for po in self.product_offerings.values():
                writer.writerow([po.id, po.name, po.inventory, po.demand, po.time_stamp])
                edges_list.append({"source": po.id, "target": po.product_family_id})

        with open(file_names["Modules"], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "inventory", "importance", "time_stamp"])
            for m in self.modules.values():
                writer.writerow([m.id, m.name, m.inventory, m.importance, m.time_stamp])
                edges_list.append({"source": m.id, "target": m.product_offering_id})

        edges_df = pd.concat([pd.DataFrame([edge]) for edge in edges_list], ignore_index=True)
        edges_df.to_csv("data/edges.csv", index=False)
