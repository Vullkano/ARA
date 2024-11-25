import pathlib

import networkx as nx
import igraph as ig
import leidenalg as la
import pandas as pd
from pathlib import Path
import numpy as np


def StudyEachCountry(country:str, current_dir:pathlib.WindowsPath) -> None:

    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    assert country in countries
    assert type(current_dir) == pathlib.WindowsPath and "Twitch" in str(current_dir)

    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    current_dir = current_dir / "data"

    Filedges = "musae_" + country + "_edges.csv"  # Nome do ficheiro de arestas
    Filetarget = "musae_" + country + "_target.csv"  # Nome do ficheiro de nodos

    edgePath = current_dir / country / Filedges  # Caminho para o ficheiro de arestas
    targetPath = current_dir / country / Filetarget  # Caminho para o ficheiro de nodos

    # ==================== #
    # Leitura dos Dados
    # ==================== #
    # Ler os dados dos nodos e arestas a partir dos ficheiros CSV
    nodos_df = pd.read_csv(targetPath)  # Dados dos nodos
    arestas_df = pd.read_csv(edgePath)  # Dados das arestas

    # ==================== #
    # Criar o Grafo
    # ==================== #
    # Criar grafo vazio em NetworkX
    G_nx = nx.Graph()

    # Adicionar os nodos ao grafo
    for _, row in nodos_df.iterrows():
        G_nx.add_node(row['new_id'],  # Identificador único do nodo
                      views=row['views'],  # Adiciona as visualizações do nodo
                      partner=row['partner'],  # Informação se o nodo é um parceiro
                      mature=row['mature'],  # Informação se o conteúdo é maduro
                      days=row['days'],  # Número de dias de atividade do nodo
                      features=row.to_dict())  # Adiciona características do nodo

    # Adicionar as arestas ao grafo
    for _, row in arestas_df.iterrows():
        G_nx.add_edge(row['from'], row['to'])  # Adiciona uma aresta entre dois nodos

    # Visualizar o número de nós e arestas
    print("Número de nós:", G_nx.number_of_nodes())  # Exibe o número total de nodos
    print("Número de arestas:", G_nx.number_of_edges())  # Exibe o número total de arestas

    # =========================== #
    # =========== LEIDEN =========== #
    # =========================== #
    # Converter o grafo de NetworkX para iGraph para usar o algoritmo de Leiden
    G_ig = ig.Graph.TupleList(G_nx.edges(), directed=False)

    # Executar o algoritmo de Leiden para detectar comunidades
    partition_leiden = la.find_partition(G_ig, la.ModularityVertexPartition)
    comunidades_leiden = partition_leiden.membership  # Obter a atribuição de comunidade para cada nodo

    # Adicionar a informação da comunidade a cada nodo no grafo de NetworkX
    for i, node in enumerate(G_ig.vs['name']):
        G_nx.nodes[int(node)]['community_leiden'] = comunidades_leiden[i]

    # Número de comunidades detectadas pelo algoritmo de Leiden
    num_comunidades_leiden = len(set(comunidades_leiden))
    print(f"Número de comunidades detetadas pelo Leiden: {num_comunidades_leiden}")

    # ==================== #
    # ============== MÉTRICAS DE CENTRALIDADE ============== #
    # ==================== #
    # 1. Centralidade de Grau
    # A centralidade de grau é uma medida do número de conexões (arestas) que um nodo tem.
    degree_centrality = nx.degree_centrality(G_nx)

    # 2. Centralidade de Proximidade
    # A centralidade de proximidade mede quão perto um nodo está de todos os outros nodos na rede.
    closeness_centrality = nx.closeness_centrality(G_nx)

    # 3. Centralidade de Intermediação
    # A centralidade de intermediação mede o quão frequentemente um nodo atua como intermediário em caminhos mais curtos entre outros nodos.
    betweenness_centrality = nx.betweenness_centrality(G_nx)

    # 4. Centralidade de Autovetor
    # A centralidade de autovetor considera não apenas o número de conexões de um nodo, mas também a importância dos nodos com os quais está conectado.
    eigenvector_centrality = nx.eigenvector_centrality(G_nx)

    # ==================== #
    # CÁLCULO DO GRAU DOS NÓS
    # ==================== #
    # O grau de um nodo representa o número de arestas conectadas a ele.
    degree = dict(G_nx.degree())

    # ==================== #
    # COEFICIENTE DE CLUSTERING
    # ==================== #
    # O coeficiente de clustering mede a tendência dos nodos de formar agrupamentos ou clusters.
    clustering_coef = nx.clustering(G_nx)

    # Coeficiente de clustering médio: média do coeficiente de clustering de todos os nodos
    avg_clustering = nx.average_clustering(G_nx)
    print(f"Coeficiente de clustering médio: {avg_clustering:.4f}")

    # ==================== #
    # ============== OUTPUT DOS RESULTADOS ============== #
    # ==================== #
    # Criar um DataFrame com as métricas de cada nodo
    df_metrics = pd.DataFrame({
        'node': list(G_nx.nodes),  # Identificadores dos nodos
        'degree': [degree[node] for node in G_nx.nodes],  # Grau de cada nodo
        'degree_centrality': [degree_centrality[node] for node in G_nx.nodes],  # Centralidade de grau
        'closeness_centrality': [closeness_centrality[node] for node in G_nx.nodes],  # Centralidade de proximidade
        'betweenness_centrality': [betweenness_centrality[node] for node in G_nx.nodes],  # Centralidade de intermediação
        'eigenvector_centrality': [eigenvector_centrality[node] for node in G_nx.nodes],  # Centralidade de autovetor
        'community_leiden': [G_nx.nodes[node]['community_leiden'] for node in G_nx.nodes],  # Comunidade do nodo
        'views': [G_nx.nodes[node]['views'] for node in G_nx.nodes],  # Visualizações do nodo
        'partner': [G_nx.nodes[node]['partner'] for node in G_nx.nodes],  # Informação de parceiro
        'mature': [G_nx.nodes[node]['mature'] for node in G_nx.nodes],  # Informação de maturidade
        'days': [G_nx.nodes[node]['days'] for node in G_nx.nodes],  # Dias de atividade
        'clustering_coef': [clustering_coef[node] for node in G_nx.nodes],  # Coeficiente de clustering
    })

    # Ordenar pelo grau de centralidade para obter os nodos mais influentes
    df_metrics_sorted = df_metrics.sort_values(by='degree_centrality', ascending=False)

    # Exibir as 5 primeiras linhas do DataFrame ordenado
    print(df_metrics_sorted.head())

    # Guardar o DataFrame num ficheiro CSV para análise posterior
    output_path_csv = current_dir / country / f"twitch_network_metrics_{country}.csv"
    df_metrics_sorted.to_csv(output_path_csv, index=False)  # Exportar os dados para CSV

    # Mostrar o caminho do CSV gerado
    print(f"Ficheiro CSV guardado em: {output_path_csv}")


if __name__ == "__main__":
    current_dir = Path.cwd()
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]
    for country in countries:
        StudyEachCountry(country, current_dir)