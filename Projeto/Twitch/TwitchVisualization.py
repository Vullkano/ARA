from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU
country = "RU"
PercNodes = 20  # 40 -> 40% dos nodos da rede

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
               views=row['views'],
               mature=row['mature'],
               partner=row['partner'],
               features=row.to_dict())  # Adiciona as características de cada nodo

# Adicionar as arestas ao grafo
for _, row in arestas_df.iterrows():
    G.add_edge(row['from'], row['to'])

# Visualizar o nº de nós e ligações
print("Número de nós:", G.number_of_nodes())
print("Número de arestas:", G.number_of_edges())

NumNodes = int(G.number_of_nodes() * (PercNodes / 100))
if NumNodes < 1500:
    NumNodes = 1500

# Desenhar uma pequena parte do grafo (cuidado para n explodir)
subgrafo = G.subgraph(list(G.nodes())[:NumNodes])

# Obter os valores de "views" para cada nodo no subgrafo
views = [subgrafo.nodes[n]['views'] for n in subgrafo.nodes]

# Definir o tamanho dos nós com base nas views (normalizando)
node_sizes = np.array(views)
node_sizes = (node_sizes - min(node_sizes)) / (max(node_sizes) - min(node_sizes))
node_sizes = 50 + (node_sizes * 1000)  # Escalar os tamanhos (mínimo de 50 e máximo de 1050)

# Ajustar o layout da rede para uma distribuição mais clara
pos = nx.spring_layout(subgrafo, k=1, iterations=50, seed=42)  # Melhor ajuste do layout com seed

# Ajustar tamanho da figura e a qualidade da visualização
plt.figure(figsize=(20, 20), dpi=300)
plt.style.use("dark_background")  # Background escuro para maior contraste

# Definir a cor dos nós com base no valor de "partner"
node_colors = ['#9146FF' if subgrafo.nodes[n]['partner'] else '#1E90FF' for n in subgrafo.nodes]

# Separar os nós com base no valor de "mature"
mature_nodes = [n for n in subgrafo.nodes if subgrafo.nodes[n]['mature'] == True]
non_mature_nodes = [n for n in subgrafo.nodes if subgrafo.nodes[n]['mature'] == False]

# Definir os tamanhos dos nós
mature_node_sizes = [node_sizes[list(subgrafo.nodes).index(n)] for n in mature_nodes]
non_mature_node_sizes = [node_sizes[list(subgrafo.nodes).index(n)] for n in non_mature_nodes]

# Desenhar nós "mature" com formato de quadrado ('s')
nx.draw_networkx_nodes(subgrafo, pos,
                       nodelist=mature_nodes,
                       node_size=mature_node_sizes,
                       node_color=[node_colors[list(subgrafo.nodes).index(n)] for n in mature_nodes],
                       node_shape='s',  # Formato de quadrado
                       edgecolors='white', linewidths=1.5,  # Borda branca
                       alpha=0.9)

# Desenhar nós "non-mature" com formato de círculo (padrão: 'o')
nx.draw_networkx_nodes(subgrafo, pos,
                       nodelist=non_mature_nodes,
                       node_size=non_mature_node_sizes,
                       node_color=[node_colors[list(subgrafo.nodes).index(n)] for n in non_mature_nodes],
                       node_shape='o',  # Formato de círculo
                       edgecolors='white', linewidths=1.5,  # Borda branca
                       alpha=0.9)

# Desenhar as arestas com maior transparência
nx.draw_networkx_edges(subgrafo, pos, alpha=0.2, edge_color='#A9A9A9')

# Adicionar legenda
legend_elements1 = [
    plt.Line2D([0], [0], marker='s', color='w', label='Mature (Quadrado)',
               markersize=15, markeredgecolor='white'),
    plt.Line2D([0], [0], marker='o', color='w', label='Non-Mature (Círculo)',
               markersize=15, markeredgecolor='white')
]

legend_elements2 = [
    plt.Line2D([0], [0], marker='v', color='w', label='Partner (Roxo)',
               markerfacecolor='#9146FF', markersize=15, markeredgecolor='white'),
    plt.Line2D([0], [0], marker='v', color='w', label='Non-Partner (Azul)',
               markerfacecolor='#1E90FF', markersize=15, markeredgecolor='white')
]

# Adicionar a primeira legenda (Mature/Non-Mature) no canto superior direito
legend1 = plt.legend(handles=legend_elements1, loc='upper right', fontsize=12, title="Mature Status")

# Adicionar a segunda legenda (Partner/Non-Partner) logo abaixo da primeira, ajustando a posição com "bbox_to_anchor"
legend2 = plt.legend(handles=legend_elements2, loc='upper right', fontsize=12, title="Partner Status",
                     bbox_to_anchor=(0.995, 0.94))  # Ajustar o valor de "0.85" para posicionar

# Re-adicionar a primeira legenda (para não ser sobrescrita pela segunda)
plt.gca().add_artist(legend1)

# Título do gráfico
plt.title(f"Subgrafo da Rede Twitch {country}", fontsize=24, color='white')

# Caminho para salvar a imagem no diretório atual
output_path = current_dir / "Imagens" / f"subgrafo_rede_twitch_{country}.png"

# Salvar o gráfico como imagem PNG
plt.savefig(output_path, bbox_inches='tight', transparent=False)

# Mostrar o gráfico
plt.show()

