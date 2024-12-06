import pandas as pd
import networkx as nx
from pathlib import Path
from community import community_louvain
import numpy as np
import scipy.stats as stats
from tqdm import tqdm
import colorama
from colorama import Fore, Style

# Inicializar colorama para suporte de cores no Windows
colorama.init()

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

    # Configuração personalizada da barra de progresso
    total_countries = len(countries)
    bar_format = (
        f"{Fore.CYAN}{{desc}}{Style.RESET_ALL}: "
        f"|{Fore.MAGENTA}{{bar:30}}{Style.RESET_ALL}| "
        f"{Fore.GREEN}{{percentage:3.0f}}%{Style.RESET_ALL} "
        f"[{Fore.BLUE}{{n_fmt}}/{total_countries}{Style.RESET_ALL}] "
        f"({Fore.YELLOW}Tempo restante: {{remaining}}{Style.RESET_ALL})"
    )

    # Iterar sobre cada país com barra de progresso personalizada
    for country in tqdm(countries, 
                       desc=" Análise das Redes Twitch", 
                       bar_format=bar_format,
                       ascii="░▒▓█",  # Preenchimento gradual com diferentes densidades
                       ncols=100):
        
        print(f"\n{Fore.CYAN}┌{'─'*50}┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} 🔍 Analisando a região: "
              f"{Fore.YELLOW}{country:^26}{Style.RESET_ALL} {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─'*50}┘{Style.RESET_ALL}")

        # Caminho do ficheiro CSV para o país atual (nós)
        nodes_path = current_dir / country / 'processed_data' / f"twitch_network_analysis_{country}.csv"
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
            G.nodes[row['node']].update(row.to_dict())

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
        eigenvector_centrality = nx.eigenvector_centrality(G)
        pagerank_centrality = nx.pagerank(G)

        avg_degree_centrality = np.mean(list(degree_centrality.values()))
        avg_betweenness_centrality = np.mean(list(betweenness_centrality.values()))
        avg_closeness_centrality = np.mean(list(closeness_centrality.values()))
        avg_eigenvector_centrality = np.mean(list(eigenvector_centrality.values()))
        avg_pagerank_centrality = np.mean(list(pagerank_centrality.values()))

        # Comunidades e modularidade
        partition = community_louvain.best_partition(G)
        modularity = community_louvain.modularity(partition, G)

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
        account_deleted_count = broadcaster_counts.get('account_Deleted', 0)
        non_streamer_count = broadcaster_counts.get('non_Streamer', 0)

        # Métricas de Centralização da Rede
        degree_centralization = max(degree_centrality.values()) - avg_degree_centrality
        betweenness_centralization = max(betweenness_centrality.values()) - avg_betweenness_centrality

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
            'Eigenvector Centrality (mean)': avg_eigenvector_centrality,
            'PageRank Centrality (mean)': avg_pagerank_centrality,
            'Number of Mature Nodes': nodes_df['mature'].sum(),
            'Number of Partner Nodes': nodes_df['partner'].sum(),
            'Number of Non-Mature Nodes': len(nodes_df) - nodes_df['mature'].sum(),
            'Number of Non-Partner Nodes': len(nodes_df) - nodes_df['partner'].sum(),
            'Average Views': avg_views,
            'Views Std': std_views,
            'Total Views': total_views,
            'Partner Broadcasters': partner_count,
            'Affiliate Broadcasters': affiliate_count,
            'Account Deleted Broadcasters': account_deleted_count,
            'Non-Streamer Broadcasters': non_streamer_count,
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

    print(f"\n{Fore.GREEN}✨ Análise completa! ✨{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Resultados guardados em: {Style.RESET_ALL}{output_path}")


if __name__ == "__main__":
    current_dir = Path.cwd()
    StudyAllCountries(current_dir)