import networkx as nx
import igraph as ig
import leidenalg as la
import community.community_louvain as community_louvain
import pandas as pd
from pathlib import Path

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU
country = "ENGB"

# ================= #
current_dir = Path.cwd()

Filedges = "musae_" + country + "_edges.csv"
Filetarget = "musae_" + country + "_target.csv"

edgePath = current_dir / country / Filedges
targetPath = current_dir / country / Filetarget

# Ler os caminhos acima
nodos_df = pd.read_csv(targetPath)
arestas_df = pd.read_csv(edgePath)

# Criar grafo vazio em NetworkX
G_nx = nx.Graph()

# Adicionar os nodos ao grafo com as visualizações de cada conta (relação entre tamanho do nodo e views)
for _, row in nodos_df.iterrows():
    G_nx.add_node(row['new_id'],
                  views=row['views'],  # Adiciona as views ao nodo
                  partner=row['partner'],  # Adiciona a informação de "partner"
                  mature=row['mature'],  # Adiciona a informação de "mature"
                  days=row['days'],  # Adiciona a informação de "days"
                  features=row.to_dict())  # Adiciona as características de cada nodo

# Adicionar as arestas ao grafo
for _, row in arestas_df.iterrows():
    G_nx.add_edge(row['from'], row['to'])

# Visualizar o nº de nós e ligações
print("Número de nós:", G_nx.number_of_nodes())
print("Número de arestas:", G_nx.number_of_edges())

# =========================== #
# =========== LEIDEN =========== #
# =========================== #

# Converter o grafo de NetworkX para iGraph
G_ig = ig.Graph.TupleList(G_nx.edges(), directed=False)

# Executar o algoritmo de Leiden
partition_leiden = la.find_partition(G_ig, la.ModularityVertexPartition)

# Obter as comunidades do Leiden
comunidades_leiden = partition_leiden.membership

# Adicionar o número da comunidade (Leiden) a cada nodo no grafo de NetworkX
for i, node in enumerate(G_ig.vs['name']):
    G_nx.nodes[int(node)]['community_leiden'] = comunidades_leiden[i]

# Número de comunidades detetadas pelo Leiden
num_comunidades_leiden = len(set(comunidades_leiden))
print(f"Número de comunidades detetadas pelo Leiden: {num_comunidades_leiden}")

# ============== MÉTRICAS DE CENTRALIDADE ============== #
# 1. Centralidade de grau
degree_centrality = nx.degree_centrality(G_nx)

# 2. Centralidade de proximidade
closeness_centrality = nx.closeness_centrality(G_nx)

# 3. Centralidade de intermediação
betweenness_centrality = nx.betweenness_centrality(G_nx)

# 4. Centralidade de autovetor
eigenvector_centrality = nx.eigenvector_centrality(G_nx)

# Mostrar as 5 contas com maior centralidade de grau
top_5_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 contas com maior centralidade de grau:", top_5_degree)

# ============== TRANSITIVIDADE ============== #
# Coeficiente de clustering (transitividade local)
clustering_coef = nx.clustering(G_nx)

# Coeficiente de clustering médio
avg_clustering = nx.average_clustering(G_nx)
print(f"Coeficiente de clustering médio: {avg_clustering:.4f}")

# ============== OUTPUT DOS RESULTADOS ============== #
# Guardar resultados principais num DataFrame para melhor visualização

# Criar um DataFrame com os nodos e as suas métricas de centralidade
df_metrics = pd.DataFrame({
    'node': list(G_nx.nodes),
    'degree_centrality': [degree_centrality[node] for node in G_nx.nodes],
    'closeness_centrality': [closeness_centrality[node] for node in G_nx.nodes],
    'betweenness_centrality': [betweenness_centrality[node] for node in G_nx.nodes],
    'eigenvector_centrality': [eigenvector_centrality[node] for node in G_nx.nodes],
    'community_leiden': [G_nx.nodes[node]['community_leiden'] for node in G_nx.nodes],
    'views': [G_nx.nodes[node]['views'] for node in G_nx.nodes],  # Adiciona as views
    'partner': [G_nx.nodes[node]['partner'] for node in G_nx.nodes],  # Adiciona o partner
    'mature': [G_nx.nodes[node]['mature'] for node in G_nx.nodes],  # Adiciona o mature
    'days': [G_nx.nodes[node]['days'] for node in G_nx.nodes],  # Adiciona os days
    'clustering_coef': [clustering_coef[node] for node in G_nx.nodes],  # Coeficiente de clustering
})

# Ordenar pelo grau de centralidade (para obter os mais influentes)
df_metrics_sorted = df_metrics.sort_values(by='degree_centrality', ascending=False)

# Mostrar o DataFrame
print(df_metrics_sorted.head())

# Guardar o DataFrame num ficheiro CSV para análise posterior
output_path_csv = current_dir / country / f"twitch_network_metrics_{country}.csv"
df_metrics_sorted.to_csv(output_path_csv, index=False)

# Mostrar o caminho do CSV gerado
print(f"Ficheiro CSV guardado em: {output_path_csv}")
