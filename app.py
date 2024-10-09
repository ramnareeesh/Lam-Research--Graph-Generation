import time

import streamlit as st
from graph_data import *
import psutil


st.header("GRAPH GENERATION MODULE", divider='')
st.write("\n")
st.write("\n")
st.write("\n")

st.subheader("_Random Graph Generator_", divider='rainbow')
no_nodes = st.number_input("Enter the number of nodes to be generated", step=1)
ratio = st.number_input("Enter the ratio modules\:parts", min_value=0.0, max_value=1.0)
max_conn = st.number_input("Enter max. no. of connections", value=5)

generate_button = st.button("Generate")

if generate_button:
    # Generate the graph and store it in session state
    graph_obj = GraphData()
    time_start = time.time()
    graph_obj = create_min_graph(graph_obj)
    G_min = graph_obj.create_graph()

    st.success("Minimum graph generated.")

    graph_obj.random_node_generator("module", int(ratio * no_nodes), max_conn)
    graph_obj.random_node_generator("part", int((1.0 - ratio) * no_nodes), max_conn)
    G = graph_obj.create_graph()
    time_end = time.time()

    st.success("Required graph generated.")
    st.metric("Time taken to generate graph", f"{time_end - time_start:.4f} seconds")

    process = psutil.Process()
    memory_info = process.memory_info()
    st.metric("Memory usage", f"{memory_info.rss / (1024 * 1024):.4f} MB")

    # Store the generated graph in session state
    st.session_state['graph'] = G
    st.session_state['graph_obj'] = graph_obj

# Only show the "Visualize Graph" button if a graph has been generated
if 'graph' in st.session_state:
    if st.button("Visualize Graph"):

        # Visualize the graph stored in session state
        st.subheader("Graph Visualization", divider='rainbow')
        time_start = time.time()
        st.plotly_chart(st.session_state['graph_obj'].visualize_graph_plotly(st.session_state['graph']))
        time_end = time.time()
        st.metric("Time taken to visualize subgraph", f"{time_end - time_start:.4f} seconds")
        process = psutil.Process()
        memory_info = process.memory_info()
        st.metric("Memory usage", f"{memory_info.rss / (1024 * 1024):.4f} MB")

    st.subheader("_Querying_", divider='rainbow')
    node_id = st.text_input("Enter the node ID to query")
    if node_id:
        if node_id in st.session_state['graph']:
            st.write("Node details:")
            st.write(st.session_state['graph'].nodes[node_id])
            if st.button("Visualize Subgraph"):
                st.write("_Visualization of subgraph_")
                time_start = time.time()
                st.plotly_chart(query_subgraph(st.session_state['graph'], node_id))
                time_end = time.time()
                st.metric("Time taken to visualize subgraph", f"{time_end - time_start:.4f} seconds")
        else:
            st.error("Node not found in the graph.")

    st.subheader("_Shortest Path_", divider='rainbow')
    source = st.text_input("Enter the source node ID")
    target = st.text_input("Enter the target node ID")
    # st.write(st.session_state['graph'].nodes[source])
    # st.write(st.session_state['graph'].nodes)
    # st.write(st.session_state['graph'].nodes[target])

    if source and target:
        st.metric(label="Shortest Path:", value=shortest_path(st.session_state['graph'], source, target))
