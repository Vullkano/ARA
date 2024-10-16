import pandas as pd
import networkx as nx
from pathlib import Path

# Definir os países a serem analisados
countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

# Caminho do diretório atual
current_dir = Path.cwd()
output_dir = current_dir / "Resultados"
output_dir.mkdir(exist_ok=True)

# Lista para armazenar resultados de cada país
results = []

# Iterar sobre cada país
for country in countries:
    print(f"Analisando o grafo do país: {country}")

    # Caminho do ficheiro CSV para o país atual (nós)
    nodes_path = current_dir / country / f"twitch_network_metrics_{country}.csv"
    # Caminho do ficheiro CSV para as arestas
    edges_path = current_dir / country / f"musae_{country}_edges.csv"

    # Ler o ficheiro CSV com os nós
    nodes_df = pd.read_csv(nodes_path)

    # Ler o ficheiro CSV com as arestas
    edges_df = pd.read_csv(edges_path)

    # Converter as variáveis booleanas para inteiros
    nodes_df['partner'] = nodes_df['partner'].astype(int)
    nodes_df['mature'] = nodes_df['mature'].astype(int)

    # Criar o grafo a partir das arestas
    G = nx.from_pandas_edgelist(edges_df, 'from', 'to')

    # Adicionar atributos dos nós ao grafo
    for index, row in nodes_df.iterrows():
        G.nodes[row['node']]['partner'] = row['partner']
        G.nodes[row['node']]['mature'] = row['mature']

    # Métricas globais
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    diameter = nx.diameter(G) if nx.is_connected(G) else None
    num_components = nx.number_connected_components(G)
    density = nx.density(G)
    avg_clustering_coeff = nx.average_clustering(G)
    avg_path_length = nx.average_shortest_path_length(G) if nx.is_connected(G) else None
    assortativity = nx.degree_assortativity_coefficient(G)

    # Contagem dos nós 'mature' e 'partner'
    num_mature = sum([1 for n, d in G.nodes(data=True) if d.get('mature') == 1])
    num_non_mature = num_nodes - num_mature
    num_partner = sum([1 for n, d in G.nodes(data=True) if d.get('partner') == 1])
    num_non_partner = num_nodes - num_partner

    # Armazenar os resultados numa lista
    results.append({
        'Country': country,
        'Number of Nodes': num_nodes,
        'Number of Edges': num_edges,
        'Number of Components': num_components,
        'Diameter': diameter,
        'Density': density,
        'Average Clustering Coefficient': avg_clustering_coeff,
        'Average Path Length': avg_path_length,
        'Assortativity': assortativity,
        'Number of Mature Nodes': num_mature,
        'Number of Non-Mature Nodes': num_non_mature,
        'Number of Partner Nodes': num_partner,
        'Number of Non-Partner Nodes': num_non_partner
    })

# Criar um DataFrame com os resultados
df_results = pd.DataFrame(results)

# Guardar os resultados num ficheiro CSV
output_path = output_dir / "network_metrics_summary.csv"
df_results.to_csv(output_path, index=False)

print(f"Análise completa! Resultados guardados em: {output_path}")
