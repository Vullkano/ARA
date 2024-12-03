import pandas as pd
import networkx as nx
from pathlib import Path
from community import community_louvain  # Para detecção de comunidades e modularidade
import numpy as np
import scipy.stats as stats

# TODO Não sei se coloco similaridade de cosseno

def StudyAllCountries(current_dir: Path) -> None:
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    assert isinstance(current_dir, Path)
    assert "Twitch" in str(current_dir)

    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    current_dir = current_dir / "data"
    output_dir = current_dir / "AllCountries"
    output_dir.mkdir(exist_ok=True)

    # Lista para armazenar resultados de cada país
    results = []

    # Iterar sobre cada país
    for country in countries:
        print(f"Analisando o grafo do país: {country}")

        # Caminho do ficheiro CSV para o país atual (nós)
        nodes_path = current_dir / country / f"twitch_network_metrics_{country}.csv"
        # Caminho do ficheiro CSV para as arestas
        edges_path = current_dir / country / f"Final_musae_{country}_edges.csv"

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
        transitivity = nx.transitivity(G)
        avg_path_length = nx.average_shortest_path_length(G) if nx.is_connected(G) else None
        assortativity = nx.degree_assortativity_coefficient(G)

        # Centralidades
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)

        avg_degree_centrality = sum(degree_centrality.values()) / len(degree_centrality)
        avg_betweenness_centrality = sum(betweenness_centrality.values()) / len(betweenness_centrality)
        avg_closeness_centrality = sum(closeness_centrality.values()) / len(closeness_centrality)

        # Comunidades e modularidade
        partition = community_louvain.best_partition(G)
        modularity = community_louvain.modularity(partition, G)

        # Contagem dos nós 'mature' e 'partner'
        num_mature = sum([1 for n, d in G.nodes(data=True) if d.get('mature') == 1])
        num_non_mature = num_nodes - num_mature
        num_partner = sum([1 for n, d in G.nodes(data=True) if d.get('partner') == 1])
        num_non_partner = num_nodes - num_partner

        # Estatísticas de Views
        views = nodes_df['views'].values
        avg_views = views.mean()
        std_views = views.std()
        total_views = views.sum()
        
        # Contagem de broadcaster_types
        broadcaster_counts = nodes_df['broadcaster_type'].value_counts()
        partner_count = broadcaster_counts.get('partner', 0)
        affiliate_count = broadcaster_counts.get('affiliate', 0)
        normal_count = broadcaster_counts.get('', 0)  # broadcasters normais têm valor vazio

        # Métricas de Centralização da Rede
        degree_centralization = max(degree_centrality.values()) - (sum(degree_centrality.values()) / len(degree_centrality))
        betweenness_centralization = max(betweenness_centrality.values()) - (sum(betweenness_centrality.values()) / len(betweenness_centrality))
        
        # Reciprocidade (importante para redes sociais)
        reciprocity = nx.reciprocity(G)
        
        # Métricas de Distribuição
        degree_values = [d for n, d in G.degree()]
        degree_std = np.std(degree_values)  # Desvio padrão dos graus
        degree_skewness = stats.skew(degree_values)  # Assimetria da distribuição
        
        # Eficiência Global da Rede
        global_efficiency = nx.global_efficiency(G)

        # Armazenar os resultados numa lista
        results.append({
            'Country': country,
            'Number of Nodes': num_nodes,
            'Number of Edges': num_edges,
            'Number of Components': num_components,
            'Diameter': diameter,
            'Density': density,
            'Average Clustering Coefficient': avg_clustering_coeff,
            'Transitivity': transitivity,
            'Average Path Length': avg_path_length,
            'Assortativity': assortativity,
            'Modularity': modularity,
            'Degree Centrality (mean)': avg_degree_centrality,
            'Betweenness Centrality (mean)': avg_betweenness_centrality,
            'Closeness Centrality (mean)': avg_closeness_centrality,
            'Number of Mature Nodes': num_mature,
            'Number of Non-Mature Nodes': num_non_mature,
            'Number of Partner Nodes': num_partner,
            'Number of Non-Partner Nodes': num_non_partner,
            'Average Views': avg_views,
            'Views Std': std_views,
            'Total Views': total_views,
            'Partner Broadcasters': partner_count,
            'Affiliate Broadcasters': affiliate_count,
            'Normal Broadcasters': normal_count,
            'Degree Centralization': degree_centralization,
            'Betweenness Centralization': betweenness_centralization,
            'Reciprocity': reciprocity,
            'Degree Std': degree_std,
            'Degree Skewness': degree_skewness,
            'Global Efficiency': global_efficiency,
        })

    # Criar um DataFrame com os resultados
    df_results = pd.DataFrame(results)

    # Guardar os resultados num ficheiro CSV
    output_path = output_dir / "network_metrics_summary.csv"
    df_results.to_csv(output_path, index=False)

    print(f"Análise completa! Resultados guardados em: {output_path}")


if __name__ == "__main__":
    current_dir = Path.cwd()
    StudyAllCountries(current_dir)

    