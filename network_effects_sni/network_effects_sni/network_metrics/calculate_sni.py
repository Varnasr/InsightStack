
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load SHG data
df = pd.read_csv('../data/shg_peer_influence.csv')

# Create edges based on shared peer group and village
edges = []
for group in df['peer_group_id'].unique():
    group_members = df[df['peer_group_id'] == group]['id'].tolist()
    edges.extend([(i, j) for i in group_members for j in group_members if i != j])

# Build the graph
G = nx.Graph()
G.add_edges_from(edges)

# Compute centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Convert to DataFrame
centrality_df = pd.DataFrame({
    'id': list(degree_centrality.keys()),
    'degree': list(degree_centrality.values()),
    'betweenness': list(betweenness_centrality.values()),
    'eigenvector': list(eigenvector_centrality.values())
})

# Merge with original data
df_metrics = df.merge(centrality_df, on='id')

# Save to CSV
df_metrics.to_csv('../network_metrics/sni_with_metrics.csv', index=False)

# Plot the network
plt.figure(figsize=(10, 8))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
plt.title('SHG Peer Group Network')
plt.savefig('../network_metrics/shg_network_plot.png', dpi=300)
plt.close()
