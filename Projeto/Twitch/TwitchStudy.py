import networkx as nx
import community.community_louvain as community_louvain
import pandas as pd
from pathlib import Path

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU

country = "PTBR"

# ================= #
current_dir = Path.cwd()

Filedges = "musae_" + country + "_edges.csv"
Filetarget = "musae_" + country + "_target.csv"

edgePath = current_dir / country / Filedges
targetPath = current_dir / country / Filetarget

# Ler os caminhos acima
nodos_df = pd.read_csv(targetPath)
arestas_df = pd.read_csv(edgePath)

# Criar grafo vazio
G = nx.Graph()

# Adicionar os nodos ao grafo com as visualizações de cada conta (relação entre tamanho do nodo e views)
for _, row in nodos_df.iterrows():
    G.add_node(row['new_id'],
               views=row['views'],  # Adiciona as views ao nodo
               features=row.to_dict())  # Adiciona as características de cada nodo

# Adicionar as arestas ao grafo
for _, row in arestas_df.iterrows():
    G.add_edge(row['from'], row['to'])

# Visualizar o nº de nós e ligações
print("Número de nós:", G.number_of_nodes())
print("Número de arestas:", G.number_of_edges())

# ============== MÉTRICAS DE CENTRALIDADE ==============
# 1. Centralidade de grau
degree_centrality = nx.degree_centrality(G)

# 2. Centralidade de proximidade
closeness_centrality = nx.closeness_centrality(G)

# 3. Centralidade de intermediação
betweenness_centrality = nx.betweenness_centrality(G)

# 4. Centralidade de autovetor
eigenvector_centrality = nx.eigenvector_centrality(G)

# Mostrar as 5 contas com maior centralidade de grau
top_5_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 contas com maior centralidade de grau:", top_5_degree)

# ============== DETEÇÃO DE COMUNIDADES ==============
# Usar o algoritmo de Louvain para deteção de comunidades
partition = community_louvain.best_partition(G)

# Adicionar o número da comunidade a cada nodo no grafo
for node, community in partition.items():
    G.nodes[node]['community'] = community

# Número de comunidades detetadas
num_comunidades = len(set(partition.values()))
print(f"Número de comunidades detetadas: {num_comunidades}")

# ============== TRANSITIVIDADE ==============
# Coeficiente de clustering (transitividade local)
clustering_coef = nx.clustering(G)

# Coeficiente de clustering médio
avg_clustering = nx.average_clustering(G)
print(f"Coeficiente de clustering médio: {avg_clustering:.4f}")

# ============== OUTPUT DOS RESULTADOS ==============
# Guardar resultados principais num DataFrame para melhor visualização

# Criar um DataFrame com os nodos e as suas métricas de centralidade
df_metrics = pd.DataFrame({
    'node': list(G.nodes),
    'degree_centrality': [degree_centrality[node] for node in G.nodes],
    'closeness_centrality': [closeness_centrality[node] for node in G.nodes],
    'betweenness_centrality': [betweenness_centrality[node] for node in G.nodes],
    'eigenvector_centrality': [eigenvector_centrality[node] for node in G.nodes],
    'community': [partition[node] for node in G.nodes],
    'clustering_coef': [clustering_coef[node] for node in G.nodes],
})

# Ordenar pelo grau de centralidade (para obter os mais influentes)
df_metrics_sorted = df_metrics.sort_values(by='degree_centrality', ascending=False)

# Mostrar o DataFrame
print(df_metrics_sorted.head())

# Guardar o DataFrame num ficheiro CSV para análise posterior
output_path_csv = current_dir / f"twitch_network_metrics_{country}.csv"
df_metrics_sorted.to_csv(output_path_csv, index=False)

# Mostrar o caminho do CSV gerado
print(f"Ficheiro CSV guardado em: {output_path_csv}")
