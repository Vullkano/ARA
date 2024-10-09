import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU
country = "PTBR"

# Caminho do diretório atual
current_dir = Path.cwd()

# Caminho do CSV com as comunidades
community_csv_path = current_dir / f"twitch_network_metrics_{country}.csv"  # O nome pode ser diferente

# Ler o CSV
df_communities = pd.read_csv(community_csv_path)

# Criar um grafo vazio
G = nx.Graph()

# Adicionar os nodos ao grafo
for index, row in df_communities.iterrows():
    G.add_node(row['node'], community=row['community'])

# Adicionar as arestas a partir do CSV original (caso tenha um CSV de arestas)
edgePath = current_dir / country / f"musae_{country}_edges.csv"
arestas_df = pd.read_csv(edgePath)

for _, row in arestas_df.iterrows():
    G.add_edge(row['from'], row['to'])

# Calcular a centralidade de grau para filtrar os nós
degree_centrality = nx.degree_centrality(G)

# Definir um limiar para a centralidade de grau
degree_threshold = 0.0025  # Ajuste este valor conforme necessário

# Filtrar os nós que têm centralidade de grau acima do limiar
filtered_nodes = [node for node, centrality in degree_centrality.items() if centrality > degree_threshold]
G_filtered = G.subgraph(filtered_nodes)

# Visualizar as comunidades do grafo filtrado
plt.figure(figsize=(12, 8))

# Obter as cores das comunidades
colors = [G_filtered.nodes[node]['community'] for node in G_filtered.nodes]

# Calcular posições dos nós
pos = nx.spring_layout(G_filtered, seed=42, k=0.7)  # Aumente k para maior dispersão

# Desenhar os nós
nx.draw_networkx_nodes(G_filtered, pos, node_color=colors, node_size=50, alpha=0.7)

# Desenhar as arestas com espessura ajustada
nx.draw_networkx_edges(G_filtered, pos, alpha=0.5, width=0.1)  # A espessura das arestas pode ser ajustada aqui

# Exibir o gráfico
plt.title(f'Visualização das Comunidades no Grafo da Twitch ({country}) - Filtrado')
plt.axis('off')  # Desligar o eixo
plt.show()
