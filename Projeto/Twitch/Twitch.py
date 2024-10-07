import pandas as pd
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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

# Desenhar uma pequena parte do grafo (cuidado para n explodir)
subgrafo = G.subgraph(list(G.nodes())[:1000])

# Obter os valores de "views" para cada nodo no subgrafo
views = [subgrafo.nodes[n]['views'] for n in subgrafo.nodes]

# Definir o tamanho dos nós com base nas views (normalizando)
node_sizes = np.array(views)  # Converte as views para um array NumPy
node_sizes = (node_sizes - min(node_sizes)) / (max(node_sizes) - min(node_sizes))  # Normalizar
node_sizes = 50 + (node_sizes * 1000)  # Escalar os tamanhos (mínimo de 20 e máximo de 300)

# Ajustar o layout da rede para uma distribuição mais clara
pos = nx.spring_layout(subgrafo, k=1)  # Aumentar k para maior dispersão dos nós

# Ajustar tamanho da figura e a qualidade da visualização
plt.figure(figsize=(15, 15), dpi=200)

# Normalizar as views para cores
normalized_views = (views - np.min(views)) / (np.max(views) - np.min(views))

# Usar um colormap (ex: viridis, plasma, coolwarm, etc.)
node_colors = plt.cm.turbo(normalized_views)  # Usar um colormap diferente

# Desenhar o grafo com o tamanho dos nós ajustado pelas views e cores
nx.draw(subgrafo, pos, with_labels=False, node_size=node_sizes, node_color=node_colors, alpha=1, edge_color='black')

# Título do gráfico
plt.title("Subgrafo da Rede Twitch", fontsize=24)

# Caminho para salvar a imagem no diretório atual
output_path = current_dir / f"subgrafo_rede_twitch{country}.png"

# Salvar o gráfico como imagem PNG
plt.savefig(output_path)

# Mostrar o gráfico
plt.show()