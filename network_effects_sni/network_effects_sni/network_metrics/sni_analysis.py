
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load SHG peer influence data
df = pd.read_csv('../data/shg_peer_influence.csv')

# Simulate edges based on peer group membership
edges = []
for group in df['peer_group_id'].unique():
    members = df[df['peer_group_id'] == group]['id'].tolist()
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            edges.append((members[i], members[j]))

# Create graph
G = nx.Graph()
G.add_edges_from(edges)

# Compute degree and centrality
degree_dict = dict(G.degree())
eigen_centrality = nx.eigenvector_centrality_numpy(G)

# Add metrics to DataFrame
df['network_degree'] = df['id'].map(degree_dict)
df['eigen_centrality'] = df['id'].map(eigen_centrality)

# Save with metrics
df.to_csv('../data/shg_with_network_metrics.csv', index=False)

# Visualize graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=100, node_color=list(eigen_centrality.values()), cmap=plt.cm.plasma)
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.title("SHG Peer Network (Node Color: Eigen Centrality)")
plt.axis('off')
plt.tight_layout()
plt.savefig('../visualizations/shg_network_visual.png')
plt.show()
