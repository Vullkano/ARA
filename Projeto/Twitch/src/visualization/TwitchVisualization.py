from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO

def seeGraph(current_dir, edgePath, targetPath, PercNodes, country):
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
                   broadcaster_type=row['broadcaster_type'],
                   features=row.to_dict())  # Adiciona as características de cada nodo

    # Adicionar as arestas ao grafo
    for _, row in arestas_df.iterrows():
        G.add_edge(row['from'], row['to'])

    NumNodes = max(int(G.number_of_nodes() * (PercNodes / 100)), 300)

    # Selecionar os nós baseado nas views (nós mais influentes)
    node_views = [(node, G.nodes[node]['views']) for node in G.nodes()]
    sorted_nodes = [node for node, views in sorted(node_views, key=lambda x: x[1], reverse=True)]
    
    # Criar subgrafo com os nós mais visualizados e seus vizinhos diretos
    selected_nodes = sorted_nodes[:NumNodes]
    neighbors = set()
    for node in selected_nodes:
        neighbors.update(G.neighbors(node))
    
    # Combinar os nós selecionados com alguns dos seus vizinhos
    final_nodes = set(selected_nodes)
    neighbor_list = list(neighbors - set(selected_nodes))
    if neighbor_list:
        additional_nodes = min(len(neighbor_list), NumNodes // 2)  # Adiciona até 50% mais nós
        final_nodes.update(neighbor_list[:additional_nodes])
    
    subgrafo = G.subgraph(list(final_nodes))

    # Obter os valores de "views" para cada nodo no subgrafo
    views = [subgrafo.nodes[n]['views'] for n in subgrafo.nodes]

    # Definir o tamanho dos nós com base nas views (normalizando)
    node_sizes = np.array(views)
    node_sizes = (node_sizes - min(node_sizes)) / (max(node_sizes) - min(node_sizes))
    node_sizes = 100 + (node_sizes * 1500)  # Escalar os tamanhos (mínimo de 50 e máximo de 1050)

    # Ajustar o layout da rede para centralizar os nós com mais views
    pos = nx.spring_layout(subgrafo, k=1, iterations=50, seed=42)
    
    # Ajustar posições baseado nas views
    weights = {node: subgrafo.nodes[node]['views'] for node in subgrafo.nodes()}
    max_weight = max(weights.values())
    
    # Normalizar pesos e ajustar posições
    for node in pos:
        # Calcular distância do centro baseado nas views (mais views = mais próximo do centro)
        weight = weights[node] / max_weight
        x, y = pos[node]
        distance = np.sqrt(x**2 + y**2)
        if distance > 0:
            # Quanto mais views, menor o fator de distância do centro
            factor = 10 - (weight/2)
            pos[node] = (x * factor * 10, y * factor * 10)
    
    # Ajustar tamanho da figura e a qualidade da visualização
    plt.figure(figsize=(20, 20), dpi=300)
    plt.style.use("dark_background")  # Background escuro para maior contraste

    # Definir a cor dos nós com base no broadcaster_type
    broadcaster_colors = {
        'partner': '#9146FF',      # Roxo Twitch
        'affiliate': '#00A9FF',    # Azul claro
        'account_Deleted': '#E91916',  # Vermelho Twitch
        'non_Streamer': '#1FE5B6',   # Verde Twitch
    }
    
    # Mapear as cores para cada nó baseado no broadcaster_type
    node_colors = []
    for n in subgrafo.nodes:
        broadcaster_type = subgrafo.nodes[n]['features'].get('broadcaster_type', '')
        # Converter para lowercase para evitar problemas de case
        broadcaster_type = broadcaster_type.lower()
        
        if broadcaster_type == 'partner':
            color = broadcaster_colors['partner']
        elif broadcaster_type == 'affiliate':
            color = broadcaster_colors['affiliate']
        elif broadcaster_type == 'account_deleted':
            color = broadcaster_colors['account_Deleted']
        elif broadcaster_type == 'non_streamer':
            color = broadcaster_colors['non_Streamer']
            
        node_colors.append(color)

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

    # Após desenhar os nós normais, adicionar imagens e labels para os top nós por views
    node_views = [(node, G.nodes[node]['views']) for node in subgrafo.nodes()]
    top_nodes = sorted(node_views, key=lambda x: x[1], reverse=True)[:3] # NumNodes para todos
    
    # Criar dicionário de labels e imagens apenas para os top nós
    labels = {}
    label_pos = pos.copy()  # Criar cópia das posições para ajustar os labels

    for node, _ in top_nodes:
        username = subgrafo.nodes[node]['features']['username']
        views = subgrafo.nodes[node]['views']
        profile_pic_url = subgrafo.nodes[node]['features']['profile_pic']
        
        # Adicionar a imagem como um nó circular
        try:
            # Baixar a imagem da URL
            response = requests.get(profile_pic_url)
            img = Image.open(BytesIO(response.content))
            
            # Converter para array numpy
            img_array = np.asarray(img)
            
            # Criar e configurar a imagem
            imagebox = OffsetImage(img_array, zoom=0.05)  # Ajuste o zoom conforme necessário
            imagebox.image.axes = plt.gca()
            
            # Criar uma anotação com a imagem
            ab = AnnotationBbox(imagebox, pos[node],
                              frameon=True,
                              pad=0,
                              box_alignment=(0.5, 0.5),
                              bboxprops=dict(facecolor='white', 
                                           edgecolor='white',
                                           alpha=0.8))
            plt.gca().add_artist(ab)
        except Exception as e:
            print(f"Não foi possível carregar a imagem para {username}: {str(e)}")
        
        # Adicionar o label com username e views
        labels[node] = f"{username}\n{views:,} views"

        # Ajustar posição do label para ficar abaixo da imagem
        x, y = pos[node]
        node_size = node_sizes[list(subgrafo.nodes).index(node)]
        offset = node_size / 800  # Ajuste este valor para controlar a distância
        label_pos[node] = (x, y - offset )  # Mover o label para baixo
    
    
    nx.draw_networkx_labels(subgrafo, label_pos,
                        labels,
                        font_size=2.5,
                        font_weight='bold',
                        font_color='white',
                        bbox=dict(facecolor='black',
                                  edgecolor='white',
                                  alpha=0.5,
                                  pad=0,
                                  boxstyle='round,pad=0'))


    # Desenhar as arestas com maior transparência
    nx.draw_networkx_edges(subgrafo, pos, alpha=0.1, edge_color='#A9A9A9')

    # Criar as legendas
    legend_elements1 = [
        plt.Line2D([0], [0], marker='s', color='w', label='Mature (Quadrado)',
                   markersize=15, markeredgecolor='white'),
        plt.Line2D([0], [0], marker='o', color='w', label='Non-Mature (Círculo)',
                   markersize=15, markeredgecolor='white')
    ]

    legend_elements2 = [
        plt.Line2D([0], [0], marker='v', color='w', label='Partner',
                   markerfacecolor='#9146FF', markersize=15, markeredgecolor='white'),
        plt.Line2D([0], [0], marker='v', color='w', label='Affiliate',
                   markerfacecolor='#00A9FF', markersize=15, markeredgecolor='white'),
        plt.Line2D([0], [0], marker='v', color='w', label='Account Deleted',
                   markerfacecolor='#E91916', markersize=15, markeredgecolor='white'),
        plt.Line2D([0], [0], marker='v', color='w', label='Non-Streamer',
                   markerfacecolor='#1FE5B6', markersize=15, markeredgecolor='white'),
    ]

    # Adicionar a primeira legenda (Mature/Non-Mature) no canto superior direito
    legend1 = plt.legend(handles=legend_elements1, loc='upper right', fontsize=12, title="Mature Status")

    # Adicionar a segunda legenda (Broadcaster Types) logo abaixo da primeira
    legend2 = plt.legend(handles=legend_elements2, loc='upper right', fontsize=12, title="Broadcaster Type",
                        bbox_to_anchor=(0.995, 0.94))

    # Re-adicionar a primeira legenda
    plt.gca().add_artist(legend1)

    # Título do gráfico
    plt.title(f"Subgrafo da Rede Twitch {country}", fontsize=24, color='white')

    # Caminho para salvar a imagem no diretório atual
    output_path = current_dir / 'docs' / "Imagens" / 'notebook2' / 'Graph' / f"subgrafo_rede_twitch_{country}.png"

    # Criar diretórios necessários para salvar o gráfico
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Desativar o grid
    plt.grid(False)
    plt.gca().grid(False)

    # Salvar o gráfico como imagem PNG
    plt.savefig(output_path, bbox_inches='tight', transparent=False)

    # Mostrar o gráfico
    plt.show()

if __name__ == "__main__":
    # ================= #
    current_dir = Path.cwd()
    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]
    for country in countries:
        Filedges = "musae_" + country + "_edges.csv"
        Filetarget = "musae_" + country + "_target.csv"

        edgePath = current_dir / 'data' / country / Filedges
        targetPath = current_dir / 'data' / country / Filetarget

        PercNodes = 15  # 40 -> 40% dos nodos da rede

        seeGraph(current_dir, edgePath, targetPath, PercNodes, country)