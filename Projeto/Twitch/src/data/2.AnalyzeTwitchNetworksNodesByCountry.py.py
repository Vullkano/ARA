import pathlib

import networkx as nx
import pandas as pd
from pathlib import Path
import numpy as np

def StudyEachCountry(country: str, current_dir: pathlib.WindowsPath) -> None:
    # Lista de países disponíveis para análise
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    # Verificar se o país especificado é válido
    assert country in countries
    # Garantir que o diretório atual é do tipo correto e contém "Twitch" no caminho
    assert type(current_dir) == pathlib.WindowsPath and "Twitch" in str(current_dir)

    # Ajustar o caminho para a raiz do diretório "Twitch"
    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    # Diretório onde estão os dados
    current_dir = current_dir / "data"

    # Nomes dos ficheiros de arestas e nodos para o país especificado
    Filedges = "musae_" + country + "_edges.csv"  # Nome do ficheiro de arestas
    Filetarget = "musae_" + country + "_target.csv"  # Nome do ficheiro de nodos

    # Caminhos completos para os ficheiros
    edgePath = current_dir / country / Filedges  # Caminho para o ficheiro de arestas
    targetPath = current_dir / country / Filetarget  # Caminho para o ficheiro de nodos

    # ==================== #
    # Leitura dos Dados
    # ==================== #
    # Ler o ficheiro de nodos para obter atributos dos utilizadores
    nodos_df = pd.read_csv(targetPath)  # Dados dos nodos
    # Ler o ficheiro de arestas para obter as conexões entre utilizadores
    arestas_df = pd.read_csv(edgePath)  # Dados das arestas

    # ==================== #
    # Criar o Grafo
    # ==================== #
    # Inicializar o grafo usando NetworkX
    G_nx = nx.Graph()

    # Adicionar nodos ao grafo com atributos associados
    for _, row in nodos_df.iterrows():
        G_nx.add_node(row['new_id'],  # Identificador único do nodo
                      views=row['views'],  # Número de visualizações do streamer
                      partner=row['partner'],  # Se o streamer é parceiro da Twitch
                      mature=row['mature'],  # Se o conteúdo é classificado como maduro
                      days=row['days'],  # Dias desde a criação da conta
                      features=row.to_dict())  # Todas as características do nodo

    # Adicionar arestas ao grafo baseadas nas conexões entre utilizadores
    for _, row in arestas_df.iterrows():
        G_nx.add_edge(row['from'], row['to'])

    print("Número de nós:", G_nx.number_of_nodes())
    print("Número de arestas:", G_nx.number_of_edges())

    # ==================== #
    # ============== MÉTRICAS DE CENTRALIDADE ============== #
    # ==================== #
    # Cálculo de várias métricas de centralidade
    degree_centrality = nx.degree_centrality(G_nx)  # Centralidade de grau
    closeness_centrality = nx.closeness_centrality(G_nx)  # Centralidade de proximidade
    betweenness_centrality = nx.betweenness_centrality(G_nx)  # Centralidade de intermediação
    eigenvector_centrality = nx.eigenvector_centrality(G_nx)  # Centralidade de vetor próprio
    pagerank_centrality = nx.pagerank(G_nx)  # Centralidade de PageRank
    katz_centrality = nx.katz_centrality(G_nx)  # Centralidade de Katz

    # ==================== #
    # CÁLCULO DO GRAU DOS NÓS
    # ==================== #
    # Obter o grau de cada nodo
    degree = dict(G_nx.degree())

    # ==================== #
    # COEFICIENTE DE CLUSTERING
    # ==================== #
    # Calcular o coeficiente de clustering para cada nodo
    clustering_coef = nx.clustering(G_nx)
    # Calcular o coeficiente de clustering médio do grafo
    avg_clustering = nx.average_clustering(G_nx)
    print(f"Coeficiente de clustering médio: {avg_clustering:.4f}")

    # ==================== #
    # ============== OUTPUT DOS RESULTADOS ============== #
    # ==================== #
    # Criar um DataFrame com métricas calculadas para cada nodo
    df_metrics = pd.DataFrame({
        'node': list(G_nx.nodes),
        'degree': [degree[node] for node in G_nx.nodes],  # Grau do nodo
        'degree_centrality': [degree_centrality[node] for node in G_nx.nodes],  # Centralidade de grau
        'closeness_centrality': [closeness_centrality[node] for node in G_nx.nodes],  # Centralidade de proximidade
        'betweenness_centrality': [betweenness_centrality[node] for node in G_nx.nodes],  # Centralidade de intermediação
        'eigenvector_centrality': [eigenvector_centrality[node] for node in G_nx.nodes],  # Centralidade de vetor próprio
        'pagerank_centrality': [pagerank_centrality[node] for node in G_nx.nodes],  # Centralidade de PageRank
        'katz_centrality': [katz_centrality[node] for node in G_nx.nodes],  # Centralidade de Katz
        'views': [G_nx.nodes[node]['views'] for node in G_nx.nodes],  # Visualizações do streamer
        'partner': [G_nx.nodes[node]['partner'] for node in G_nx.nodes],  # Status de parceiro
        'mature': [G_nx.nodes[node]['mature'] for node in G_nx.nodes],  # Status de conteúdo maduro
        'days': [G_nx.nodes[node]['days'] for node in G_nx.nodes],  # Dias desde a criação da conta
        'clustering_coef': [clustering_coef[node] for node in G_nx.nodes],  # Coeficiente de clustering
    })

    # Ordenar os nodos por centralidade de grau
    df_metrics_sorted = df_metrics.sort_values(by='degree_centrality', ascending=False)
    print(df_metrics_sorted.head())

    # Guardar os resultados num ficheiro CSV
    output_path_csv = current_dir / country / f"twitch_network_metrics_{country}.csv"
    df_metrics_sorted.to_csv(output_path_csv, index=False)
    print(f"Ficheiro CSV guardado em: {output_path_csv}")

if __name__ == "__main__":
    # Diretório atual
    current_dir = Path.cwd()
    # Lista de países a analisar
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]
    # Analisar cada país na lista
    for country in countries:
        StudyEachCountry(country, current_dir)
