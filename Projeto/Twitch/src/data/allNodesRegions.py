from pathlib import Path

import colorama
import networkx as nx
import numpy as np
import pandas as pd
import scipy.stats as stats
from colorama import Fore, Style
from community import community_louvain
from tqdm import tqdm

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

    # Lista de categorias que não são videojogos
    non_Videojogos = ['IRL', 'Just Chatting', 'Watch TV', 'Art', 'Music',
                      'Science & Technology', 'Software and Game Development',
                      'Co-working & Studying', 'Crypto', 'Politics',
                      'Talk Shows & Podcasts', 'DJs', 'Special Events',
                      'Sports', 'Food & Drink', 'Casino', 'CooKing',
                      'Poker', 'Virtual Casino', 'Tabletop RPGs']

    non_Videojogos = [Njogo.strip().lower() for Njogo in non_Videojogos]

    jogos_offline = ["The Callisto Protocol", "Kingdom Two Crowns", "My Hotel", "Disco Elysium",
                     "Divinity: Original Sin II", "Grand Theft Auto: San Andreas", "osu!",
                     "The Binding of Isaac: Repentance", "God of War Ragnarök", "BUCKSHOT ROULETTE", "Atomic Heart",
                     "Gothic II", "Grand Theft Auto III", "Silent Hill 2", "Ghostwire: Tokyo", "DREDGE",
                     "VLADiK BRUTAL", "Northern Journey", "The Dark Pictures Anthology: Little Hope",
                     "Marvel's Spider-Man", "Resident Evil 4", "Crossout", "Horizon Zero Dawn Remastered", "Outlast II",
                     "The Last of Us Part I", "Neva", "Risk of Rain 2", "ELDEN RING", "Alan Wake II",
                     "DARK SOULS II: Scholar of the First Sin", "DARK SOULS III", "Dark Souls: Remastered", "Diablo II",
                     "Fallout 4", "Dungeon Crusher: Soul Hunters", "Castlevania: Dawn of Sorrow", "Artifact",
                     "I Wanna Kill the Kamilia 3", "Torchlight: Infinite", "The Guild 3", "Sid Meier's Civilization VI",
                     "Sons of the Forest", "The Sims 4", "X4: Foundations", "Hades II",
                     "Prince of Persia: The Lost Crown", "Bloodborne", "Angry Birds VR: Isle of Pigs",
                     "Heroes of Might and Magic V", "Internet Cafe Simulator 2", "Wolfenstein: The New Order",
                     "Factorio", "DOOM Eternal", "Everlasting Summer", "God Hand", "Beyond: Two Souls", "Mafia III",
                     "Zenless Zone Zero", "Stardew Valley", "SIFU", "Dead Space 3", "Mafia II", "Fallout 2",
                     "SnowRunner", "Hollow Knight", "The Witcher 3: Wild Hunt", "Killer Instinct", "Little Misfortune",
                     "Magicraft", "Magicraft", "Planetbase", "Microsoft Flight Simulator 2024", "Songs of Conquest",
                     "Stalker 2", "Amnesia: Rebirth", "Napoleon: Total War", "Gran Saga", "Pokémon Emerald Version",
                     "Football, Tactics & Glory", "Katamari Damacy REROLL", "Lethal Company",
                     "Vampire: The Masquerade - Bloodlines", "Red Dead Redemption", "The Walking Dead",
                     "Detroit: Become Human", "Until Dawn", "DiRT Rally 2.0", "Portal 2", "Rise of the Tomb Raider",
                     "Half-Life: Alyx", "Cyberpunk 2077", "Forza Horizon 5", "South Park: The Fractured But Whole",
                     "TSIOQUE", "Need for Speed: Most Wanted", "inFAMOUS: Second Son", "Marvel's Spider-Man Remastered",
                     "Alone in the Dark", "Lobotomy Corporation", "Mortal Kombat 1", "Tropico 6", "Dark and Darker",
                     "Gray Zone Warfare", "The Dark Pictures Anthology: Man of Medan", "Beat Saber", "Blasphemous",
                     "Baldur's Gate 3", "Broken Arrow", "Yakuza 0", "Dishonored", "Hogwarts Legacy",
                     "Grand Theft Auto IV", "Need for Speed: Underground 2", "Only Up!", "Dragon Age: Origins",
                     "Breathedge", "Lucky Tower Ultimate", "Prey", "Euro Truck Simulator 2", "Pathfinder: Kingmaker",
                     "Empire of the Ants", "The Dark Pictures Anthology: The Devil in Me", "Tiny Bunny",
                     "Vintage Story", "The Surfer", "Batman: The Enemy Within", "Wolfenstein II: The New Colossus",
                     "No Man's Sky", "Cities: Skylines", "Valhall", "The Witcher 2: Assassins of Kings",
                     "Amnesia: The Dark Descent", "Hollow Knight: Silksong", "Shadow of the Colossus",
                     "Red Dead Redemption 2", "Mass Effect Legendary Edition", "Sekiro: Shadows Die Twice",
                     "Journey", "The Elder Scrolls IV: Oblivion", "The Elder Scrolls III: Morrowind",
                     "Outer Wilds", "The Elder Scrolls Online", "The Elder Scrolls V: Skyrim Special Edition",
                     "Nier: Automata", "The Witcher: Enhanced Edition", "The Witcher 2: Assassins of Kings Enhanced Edition",
                     "Ori and the Will of the Wisps", "The Witcher 3: Wild Hunt - Game of the Year Edition",
                     "Control", "The Witcher 3: Wild Hunt - Blood and Wine", "The Witcher 3: Wild Hunt - Hearts of Stone",
                     "Metro Exodus", "The Legend of Zelda: Breath of the Wild",
                     "Dead Cells", "Subnautica", "The Elder Scrolls V: Skyrim"]

    jogos_offline = [jogo.strip().lower() for jogo in jogos_offline]

    # Iterar sobre cada país com barra de progresso personalizada
    for country in tqdm(countries,
                        desc=" Análise das Redes Twitch",
                        bar_format=bar_format,
                        ascii="░▒▓█",  # Preenchimento gradual com diferentes densidades
                        ncols=100):

        print(f"\n{Fore.CYAN}┌{'─' * 50}┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Style.RESET_ALL} 🔍 Analisando a região: "
              f"{Fore.YELLOW}{country:^26}{Style.RESET_ALL} {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─' * 50}┘{Style.RESET_ALL}")

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
        radius = nx.radius(G) if nx.is_connected(G) else None
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
        account_deleted_count = broadcaster_counts.get('account_Deleted', 0)
        non_streamer_count = broadcaster_counts.get('non_Streamer', 0)

        # Métricas de Centralização da Rede
        degree_centralization = max(degree_centrality.values()) - avg_degree_centrality
        betweenness_centralization = max(betweenness_centrality.values()) - avg_betweenness_centrality

        # Métricas de Distribuição
        degree_values = [d for n, d in G.degree()]
        degree_std = np.std(degree_values)  # Desvio padrão dos graus

        # Eficiência Global da Rede
        global_efficiency = nx.global_efficiency(G)

        # Ajuste na parte onde se atribui a categoria GameType
        def categorize_game(x: str) -> str:
            # Verificar se o nome do jogo não é nulo e compará-lo com as listas fornecidas
            if pd.isna(x):
                return np.nan
            game_name = x.strip().lower()  # Remove espaços extras e converte para minúsculas
            if game_name in jogos_offline:
                return 'Offline'
            elif game_name in non_Videojogos:
                return 'Non-Videogame'
            else:
                return 'Online'

        # Aplicar a função de categorização aos jogos
        nodes_df['GameType'] = nodes_df['game_name'].apply(categorize_game)

        # Contagens por categoria
        OFF_videogames_count = nodes_df[nodes_df['GameType'] == 'Offline'].shape[0]
        non_videogames_count = nodes_df[nodes_df['GameType'] == 'Non-Videogame'].shape[0]
        ON_videogames_count = nodes_df[nodes_df['GameType'] == 'Online'].shape[0]

        # Contar os valores NaN na coluna GameType
        nan_count = nodes_df['GameType'].isna().sum()

        # Obter a maior componente conectada (componente gigante)
        largest_component = max(nx.connected_components(G), key=len)
        G_giant = G.subgraph(largest_component).copy()

        # Número de nós e arestas da componente gigante
        num_nodes_giant = G_giant.number_of_nodes()
        num_edges_giant = G_giant.number_of_edges()

        # Calculando a heterogeneidade dos graus
        mean_deg = np.mean(degree_values)
        mean_deg_squared = np.mean(np.array(degree_values) ** 2)
        heterogeneity = mean_deg_squared / mean_deg ** 2

        # Calcular o k-core
        k_core = nx.k_core(G)

        # Obter a quantidade de nós e arestas no k-core
        num_nodos_k_core = k_core.number_of_nodes()  # Número de nós
        num_arestas_k_core = k_core.number_of_edges()  # Número de arestas

        # Armazenar os resultados numa lista
        results.append({
            'Country': country,
            'Number of Nodes': num_nodes,
            'Number of Edges': num_edges,
            'Diameter': diameter,
            'Radius': radius,
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
            'Average Views': avg_views,
            'Views Std': std_views,
            'Total Views': total_views,
            'Degree Centralization': degree_centralization,
            'Betweenness Centralization': betweenness_centralization,
            'Degree Std': degree_std,
            'Global Efficiency': global_efficiency,
            'Heterogeneity': heterogeneity,
            'Giant Component Nodes': num_nodes_giant,
            'Giant Component Edges': num_edges_giant,
            'Number of Nodes in K-Core': num_nodos_k_core,
            'Number of Edges in K-Core': num_arestas_k_core,
            'On-Videogame Channels': ON_videogames_count,
            'Off-Videogame Channels': OFF_videogames_count,
            'Non-Videogame Channels': non_videogames_count,
            'Non-Content': nan_count,
            'Partner Broadcasters': partner_count,
            'Affiliate Broadcasters': affiliate_count,
            'Account Deleted Broadcasters': account_deleted_count,
            'Non-Streamer Broadcasters': non_streamer_count,
            'Number of Mature Nodes': nodes_df['mature'].sum(),
            'Number of Partner Nodes': nodes_df['partner'].sum(),
            'Number of Non-Mature Nodes': len(nodes_df) - nodes_df['mature'].sum(),
            'Number of Non-Partner Nodes': len(nodes_df) - nodes_df['partner'].sum(),
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
    print(current_dir)
    StudyAllCountries(current_dir)
