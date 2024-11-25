import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import pathlib


def getCommunities(country:str, filter_mature:bool = False, filter_partner:bool = False, current_dir:pathlib.WindowsPath = Path.cwd()):

    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    assert country in countries
    assert type(current_dir) == pathlib.WindowsPath and "Twitch" in str(current_dir)
    assert type(filter_mature) == type(filter_partner) == bool
    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    # Caminho do CSV com as comunidades
    community_csv_path = current_dir / 'data' / country / f"twitch_network_metrics_{country}.csv"

    # Ler o CSV
    df_communities = pd.read_csv(community_csv_path)

    # Aplicar filtros, se necessário
    if filter_mature:
        df_communities = df_communities[df_communities['mature'] == True]
    if filter_partner:
        df_communities = df_communities[df_communities['partner'] == True]

    # Criar um grafo vazio
    G = nx.Graph()

    # Adicionar os nodos ao grafo
    for index, row in df_communities.iterrows():
        G.add_node(row['node'], community=row['community_leiden'])

    # Adicionar as arestas a partir do CSV original (caso tenha um CSV de arestas)
    edgePath = current_dir / country / f"musae_{country}_edges.csv"
    arestas_df = pd.read_csv(edgePath)

    # Adicionar as arestas apenas entre nós que passaram nos filtros
    for _, row in arestas_df.iterrows():
        if row['from'] in G.nodes and row['to'] in G.nodes:
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

    # Ajustar o tamanho da figura e a qualidade da visualização
    plt.figure(figsize=(20, 20), dpi=300)
    plt.style.use("dark_background")  # Estilo de fundo escuro

    # Desenhar os nós
    nx.draw_networkx_nodes(G_filtered, pos, node_color=colors, node_size=50, alpha=0.7)

    # Desenhar as arestas com espessura ajustada
    nx.draw_networkx_edges(G_filtered, pos, alpha=0.2, width=0.2, edge_color='#A9A9A9')

    # Exibir o gráfico
    plt.title(f'Visualização das Comunidades no Grafo da Twitch ({country}) - Filtrado', fontsize=24, color='white')
    plt.axis('off')  # Desligar o eixo

    # Caminho para salvar a imagem no diretório atual
    output_path = current_dir / 'docs' / "Imagens" / 'comunidades' / f"Comunidades_rede_twitch_{country}.png"

    # Verificar se a pasta "Imagens" existe, caso contrário, criá-la
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Salvar o gráfico como imagem PNG com fundo preto
    plt.savefig(output_path, bbox_inches='tight', transparent=False, facecolor='black')

    plt.show()

if __name__ == "__main__":
    # Escolher entre: DE, ENGB, ES, FR, PTBR, RU
    country = "ENGB"

    getCommunities(country, filter_mature=True, filter_partner=True)