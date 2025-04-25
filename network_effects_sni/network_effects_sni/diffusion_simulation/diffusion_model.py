
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load SHG data and simulate edges
df = pd.read_csv('../data/shg_peer_influence.csv')
edges = []
for group in df['peer_group_id'].unique():
    members = df[df['peer_group_id'] == group]['id'].tolist()
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            edges.append((members[i], members[j]))

# Build graph
G = nx.Graph()
G.add_edges_from(edges)

# Simulate diffusion using a threshold model
# Initialize: one seed node starts with the info
seed_node = random.choice(list(G.nodes))
activated = set([seed_node])
newly_activated = set([seed_node])
threshold = 0.3  # 30% of neighbors required to adopt

iterations = [list(activated)]

# Iterate until no new activations
while newly_activated:
    next_activated = set()
    for node in G.nodes:
        if node in activated:
            continue
        neighbors = list(G.neighbors(node))
        if not neighbors:
            continue
        active_neighbors = sum(1 for n in neighbors if n in activated)
        if active_neighbors / len(neighbors) >= threshold:
            next_activated.add(node)
    newly_activated = next_activated
    activated.update(newly_activated)
    iterations.append(list(activated))

# Plot final diffusion state
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, nodelist=G.nodes, node_color=['orange' if n in activated else 'lightgray' for n in G.nodes], node_size=100)
nx.draw_networkx_edges(G, pos, alpha=0.4)
plt.title("Final State of Diffusion (Threshold = 30%)")
plt.axis('off')
plt.tight_layout()
plt.savefig('../visualizations/diffusion_simulation.png')
plt.show()

# Save log of diffusion rounds
with open('../diffusion_simulation/diffusion_log.txt', 'w') as f:
    for i, step in enumerate(iterations):
        f.write(f"Step {i}: {len(step)} activated nodes\n")
