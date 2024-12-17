import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import powerlaw
import matplotlib.patheffects as pe


def setup_style():
    """Configuração global do estilo dos gráficos"""
    plt.style.use('dark_background')
    sns.set_palette("colorblind")
    plt.rcParams.update({
        'figure.figsize': (12, 8),
        'axes.titlesize': 18,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'axes.grid': False
    })

# Função para criar subpastas para cada tipo de gráfico
def create_subfolder(folder_name, output_dir):
    subfolder = output_dir / folder_name
    subfolder.mkdir(exist_ok=True)
    return subfolder

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

##### ======================== Ficheiro 0 ======================== #####

def plot_broadcaster_distribution(df, country, output_dir):
    """
    Cria um gráfico circular mostrando a distribuição dos tipos de broadcasters
    
    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(10, 8))
    broadcaster_counts = df['broadcaster_type'].value_counts()
    print(broadcaster_counts)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    plt.pie(broadcaster_counts.values, 
            labels=broadcaster_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            shadow=True,
            startangle=90,
            explode=[0.05] * len(broadcaster_counts))
    
    plt.title(f'Distribuição de Broadcaster Type - {country}', 
              pad=20, 
              fontsize=14, 
              fontweight='bold')
    
    plt.axis('equal')

    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    folder = create_subfolder('NoteBook0', output_dir)
    
    save_plot(fig, 'broadcaster_distribution', country, folder, 'pie')

def plot_game_categories(df, country, output_dir, top_n=25):
    """
    Cria um gráfico de barras horizontal com as categorias mais populares
    
    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
        top_n (int): Número de categorias a mostrar
    """
    plt.figure(figsize=(14, 10))
    
    game_counts = df['game_name'].value_counts().head(top_n)
    
    ax = sns.barplot(
        x=game_counts.values,
        y=game_counts.index,
        hue=game_counts.index,
        legend=False,
        alpha=0.8
    )
    
    plt.title(f'Top {top_n} Categorias Mais Populares - {country}', 
              pad=20, 
              fontsize=16, 
              fontweight='bold')
    plt.xlabel('Quantidade de Streams', fontsize=12, labelpad=10)
    
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    
    for i, v in enumerate(game_counts.values):
        ax.text(v + 0.5, i, f'{v:,}', 
                va='center',
                fontsize=10,
                fontweight='bold',
                color='white')
    
    plt.xlim(0, max(game_counts.values) * 1.1)
    plt.yticks(fontsize=10)
    sns.despine()
    plt.tight_layout()

    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()

    folder = create_subfolder('NoteBook0', output_dir)
    
    save_plot(fig, 'game_categories', country, folder, 'barplots')

def plot_null_distribution(df, country, output_dir):
    """
    Cria um gráfico de barras mostrando a distribuição de valores nulos por coluna
    
    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
    """
    # Contagem de nulos
    null_counts = df.isnull().sum()
    
    # Criar figura com resolução maior
    plt.figure(figsize=(12, 8), dpi=100)
    
    # Criar o grfico de barras
    ax = sns.barplot(
        x=null_counts.values,
        y=null_counts.index,
        palette='viridis',
        hue=null_counts.index,
        legend=False,
        alpha=0.8
    )
    
    # Personalizar o título e labels
    plt.title('Distribuição de Valores Nulos por Coluna', 
              pad=20, 
              fontsize=14, 
              fontweight='bold')
    plt.xlabel('Número de Valores Nulos', fontsize=12)
    plt.ylabel('Colunas', fontsize=12)
    
    # Adicionar grid apenas no eixo x
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adicionar os valores nas barras com formatação melhorada
    for i, v in enumerate(null_counts.values):
        ax.text(v + 1, i, f'{v:,}', 
                va='center',
                fontsize=10,
                fontweight='bold',
                color='white')  # Mudei para branco para manter consistência com o tema dark
    
    # Remover as bordas do gráfico
    sns.despine()
    
    # Ajustar o layout
    plt.tight_layout()

    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    folder = create_subfolder('NoteBook0', output_dir)
    
    save_plot(fig, 'null_distribution', country, folder, 'barplots')

def plot_mature_content(df, country, output_dir):
    """
    Cria um gráfico circular da distribuição de conteúdo mature/non-mature
    
    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(10, 8))
    mature_counts = df['mature'].value_counts()
    print(mature_counts)
    
    colors = ['#FF6B6B', '#4ECDC4']
    plt.pie(mature_counts.values,
            labels=['Non-Mature', 'Mature'],
            autopct='%1.1f%%',
            colors=colors,
            shadow=True,
            explode=[0.05, 0])
    
    plt.title(f'Distribuição de Conteúdo Mature - {country}')
    plt.axis('equal')
    
    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()

    folder = create_subfolder('NoteBook0', output_dir)
    
    save_plot(fig, 'mature_content', country, folder, 'pie')

def create_subfolder(folder_name, output_dir):
    """Função para criar subpastas"""
    subfolder = output_dir / folder_name
    subfolder.mkdir(exist_ok=True)
    return subfolder

def save_plot(fig, name, country, output_dir, subfolder):
    """Função auxiliar para salvar gráficos"""
    folder = create_subfolder(subfolder, output_dir)
    fig.savefig(
        folder / f"{name}_{country}.png",
        bbox_inches='tight',
        dpi=300,
        transparent=False,  # Alterado para False para manter o fundo preto
        facecolor='black'  # Adicionado para garantir o fundo preto
    )
    plt.close(fig)

## ================ Ficheiro 1 ================ ##

def plot_content_type_comparison(df, output_dir):
    """
    Cria um gráfico de barras acumulativo comparando canais de videojogos e não-videojogos por país.
    """
    setup_style()  # Certifica-te de que esta função está implementada corretamente.

    # Preparar dados para o gráfico
    content_counts = df.groupby('Country')[['On-Videogame Channels', 'Off-Videogame Channels', 
                                             'Non-Videogame Channels', 'Non-Content']].sum()

    # Criar figura
    plt.figure(figsize=(14, 8))

    # Posições das barras
    x = np.arange(len(content_counts))

    # Escolher uma paleta de cores agradável
    color_palette = sns.color_palette("Set3", len(content_counts.columns))

    # Criar barras empilhadas
    bottom = np.zeros(len(content_counts))
    for i, content_type in enumerate(content_counts.columns):
        # Criar as barras
        bars = plt.bar(x, content_counts[content_type], bottom=bottom, label=content_type, 
                       color=color_palette[i], alpha=0.85, edgecolor='black', linewidth=1.2)
        bottom += content_counts[content_type].values

        # Adicionar rótulos dentro das barras, no meio
        for j, bar in enumerate(bars):
            # Calcular a posição do meio da barra
            x_pos = bar.get_x() + bar.get_width() / 2
            y_pos = bar.get_height() / 2 + bar.get_y()  # Posição vertical no meio da barra
            plt.text(x_pos, y_pos, f'{int(bar.get_height()):,}', ha='center', va='center', 
                     fontweight='bold', fontsize=10, color='white')

    # Personalizar gráfico
    plt.title('Distribuição de Tipos de Conteúdo por País', fontsize=18, pad=20, fontweight='bold')
    plt.ylabel('Número de Canais', fontsize=14)
    plt.xticks(x, content_counts.index, rotation=45, ha='right', fontsize=12)

    # Adicionar legenda
    plt.legend(title='Content Type', fontsize=12, title_fontsize=13)

    # Adicionar grid
    plt.grid(True, axis='y', alpha=0.3)

    # Ajustar layout
    plt.tight_layout()

    # Guardar uma cópia da figura atual
    fig = plt.gcf()

    # Mostrar o gráfico
    plt.show()

    # Criar pasta e salvar (certifica-te que estas funções existem)
    folder = create_subfolder('NoteBook1', output_dir)
    save_plot(fig, 'content_type_comparison', 'all_countries', folder, 'barplots')


def count_null_usernames(countries, directory):
    """
    Conta a quantidade de usernames nulos em cada ficheiro Raw_musae_{country}_target.csv
    
    Args:
        countries (list): Lista com os códigos dos países
        
    Returns:
        dict: Dicionário com o país e quantidade de usernames nulos
    """
    null_counts = {}
    
    for country in countries:
        # Construir o caminho do ficheiro
        file_path = f'{directory}/data/{country}/processed_data/Raw_musae_{country}_target.csv'
        
        try:
            # Ler o ficheiro
            df = pd.read_csv(file_path)
            
            # Contar usernames nulos
            null_count = df['username'].isnull().sum()
            
            # Guardar no dicionário
            null_counts[country] = null_count
            
            print(f"{country}: {null_count} usernames nulos")
            
        except FileNotFoundError:
            print(f"Ficheiro não encontrado para {country}")
        except Exception as e:
            print(f"Erro ao processar {country}: {str(e)}")
            
    return null_counts

def plot_null_usernames(countries, directory, output_dir):
    """
    Cria um gráfico de barras mostrando a quantidade de usernames nulos por país
    
    Args:
        countries (list): Lista com os códigos dos países
        directory (Path): Diretório base do projeto
        output_dir (Path): Diretório para salvar as imagens
    """
    setup_style()
    plt.figure(figsize=(12, 8))
    
    # Obter os dados
    null_counts = count_null_usernames(countries, directory)
    
    # Criar o gráfico de barras
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFB347', '#A47786']
    ax = plt.bar(null_counts.keys(), null_counts.values(), color=colors, alpha=0.8)
    
    # Adicionar título e labels
    plt.title('Quantidade de Usernames Nulos por País', 
             pad=20, 
             fontsize=16, 
             fontweight='bold')
    
    plt.xlabel('País', fontsize=12, labelpad=10)
    plt.ylabel('Quantidade de Usernames Nulos', fontsize=12, labelpad=10)
    
    # Adicionar grid suave
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    
    # Adicionar valores em cima das barras
    for i, v in enumerate(null_counts.values()):
        plt.text(i, v + (max(null_counts.values()) * 0.01), 
                f'{v:,}',
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold',
                color='white')
    
    # Rotação dos labels do eixo x
    plt.xticks(rotation=0, fontsize=10)
    plt.yticks(fontsize=10)
    
    # Remover bordas
    sns.despine()
    
    # Ajustar layout
    plt.tight_layout()
    
    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook1', output_dir)
    save_plot(fig, 'null_usernames', 'all_countries', folder, 'barplots')
def plot_broadcaster_types_by_country(df, output_dir):
    """
    Cria um gráfico de barras empilhadas mostrando a distribuição dos tipos de broadcasters por país
    
    Args:
        df (DataFrame): DataFrame com os dados do network_metrics_summary.csv
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(14, 8))
    
    # Definir esquema de cores elegante
    colors = {
        'Partner': '#FF6B6B',      # Rosa coral
        'Affiliate': '#4ECDC4',    # Turquesa
        'Account Deleted': '#45B7D1',  # Azul claro
        'Non-Streamer': '#96CEB4'   # Verde menta
    }
    
    # Criar as barras empilhadas
    bottom = np.zeros(len(df))
    
    categories = [
        ('Partner Broadcasters', 'Partner'),
        ('Affiliate Broadcasters', 'Affiliate'),
        ('Account Deleted Broadcasters', 'Account Deleted'),
        ('Non-Streamer Broadcasters', 'Non-Streamer')
    ]
    
    for col, category in categories:
        values = df[col]
        plt.bar(df['Country'], values, bottom=bottom, 
                label=category, color=colors[category], 
                alpha=0.8, width=0.7)
        
        # Adicionar valores no centro de cada barra com fundo
        for i in range(len(df)):
            if values[i] > 50:  # Só mostrar texto se a área for grande o suficiente
                y_pos = bottom[i] + values[i]/2
                plt.text(i, y_pos, f'{int(values[i]):,}',
                        ha='center', va='center',
                        fontweight='bold', fontsize=10,
                        color='white',
                        bbox=dict(
                            facecolor='black',
                            alpha=0.7,
                            edgecolor='none',
                            pad=3,
                            boxstyle='round,pad=0.5'
                        ))
        bottom += values
    
    # Personalizar o gráfico com fundo no título
    plt.title('Distribuição de Tipos de Broadcasters por País',
              fontsize=20, pad=20, fontweight='bold',
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=10,
                  boxstyle='round,pad=0.8'
              ))
    
    # Labels dos eixos com fundo
    plt.xlabel('País', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    plt.ylabel('Número de Broadcasters', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    # Adicionar grid suave
    plt.grid(True, axis='y', alpha=0.2, linestyle='--')
    
    # Personalizar a legenda com fundo
    legend = plt.legend(bbox_to_anchor=(1.05, 1), 
                       loc='upper left',
                       frameon=True, 
                       facecolor='black',
                       edgecolor='none', 
                       fontsize=12)
    legend.get_frame().set_alpha(0.7)
    
    # Ajustar os limites e rotação dos rótulos
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Adicionar valores totais no topo com fundo
    for i in range(len(df)):
        total = bottom[i]
        plt.text(i, total + (total * 0.02), f'Total: {int(total):,}',
                ha='center', va='bottom',
                fontweight='bold', fontsize=12,
                color='white',
                bbox=dict(
                    facecolor='black',
                    alpha=0.7,
                    edgecolor='none',
                    pad=3,
                    boxstyle='round,pad=0.5'
                ))
    
    # Remover as bordas
    sns.despine()
    
    # Ajustar o layout
    plt.tight_layout()
    
    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook1', output_dir)
    save_plot(fig, 'broadcaster_types_distribution', 'all_countries', folder, 'barplots')

def plot_broadcaster_types_ribbon(df, output_dir):
    """
    Cria um ribbon plot (área empilhada) mostrando a distribuição dos tipos de broadcasters por país
    
    Args:
        df (DataFrame): DataFrame com os dados do network_metrics_summary.csv
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(14, 8))
    
    # Definir esquema de cores elegante com gradientes
    colors = {
        'Partner': '#FF6B6B',      # Rosa coral
        'Affiliate': '#4ECDC4',    # Turquesa
        'Account Deleted': '#45B7D1',  # Azul claro
        'Non-Streamer': '#96CEB4'   # Verde menta
    }
    
    categories = [
        ('Partner Broadcasters', 'Partner'),
        ('Affiliate Broadcasters', 'Affiliate'),
        ('Account Deleted Broadcasters', 'Account Deleted'),
        ('Non-Streamer Broadcasters', 'Non-Streamer')
    ]
    
    # Criar o ribbon plot
    x = range(len(df))
    bottom = np.zeros(len(df))
    
    for col, category in categories:
        values = df[col].values
        plt.fill_between(x, bottom, bottom + values,
                        label=category,
                        color=colors[category],
                        alpha=0.8,
                        linewidth=2,
                        edgecolor='white')
        
        # Adicionar valores no centro de cada área com fundo
        for i in range(len(df)):
            if values[i] > 50:  # Só mostrar texto se a área for grande o suficiente
                y_pos = bottom[i] + values[i]/2
                plt.text(i, y_pos, f'{int(values[i]):,}',
                        ha='center', va='center',
                        fontweight='bold', fontsize=10,
                        color='white',
                        bbox=dict(
                            facecolor='black',
                            alpha=0.7,
                            edgecolor='none',
                            pad=3,
                            boxstyle='round,pad=0.5'
                        ))
        
        bottom += values
    
    # Personalizar o gráfico com fundo no título
    plt.title('Distribuição de Tipos de Broadcasters por País',
              fontsize=20, pad=20, fontweight='bold',
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=10,
                  boxstyle='round,pad=0.8'
              ))
    
    # Labels dos eixos com fundo
    plt.xlabel('País', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    plt.ylabel('Número de Broadcasters', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    # Configurar eixo X
    plt.xticks(x, df['Country'], rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Adicionar grid suave
    plt.grid(True, axis='y', alpha=0.2, linestyle='--', zorder=0)
    
    # Personalizar a legenda com fundo
    legend = plt.legend(bbox_to_anchor=(1.05, 1), 
                       loc='upper left',
                       frameon=True, 
                       facecolor='black',
                       edgecolor='none', 
                       fontsize=12)
    legend.get_frame().set_alpha(0.7)
    
    # Adicionar valores totais no topo com fundo
    for i in range(len(df)):
        total = bottom[i]
        plt.text(i, total + (total * 0.02), f'Total: {int(total):,}',
                ha='center', va='bottom',
                fontweight='bold', fontsize=12,
                color='white',
                bbox=dict(
                    facecolor='black',
                    alpha=0.7,
                    edgecolor='none',
                    pad=3,
                    boxstyle='round,pad=0.5'
                ))
    
    # Remover as bordas
    sns.despine()
    
    # Ajustar o layout
    plt.tight_layout()
    
    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook1', output_dir)
    save_plot(fig, 'broadcaster_types_ribbon', 'all_countries', folder, 'ribbonplots')

def plot_mature_nodes_distribution(df, output_dir):
    """
    Cria um gráfico de barras empilhadas mostrando a distribuição de nodes mature/non-mature por país
    
    Args:
        df (DataFrame): DataFrame com os dados do network_metrics_summary.csv
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(14, 8))
    
    # Cores mais vibrantes mas mantendo o esquema original
    colors = {
        'Mature': '#4A90E2',    # Azul mais vibrante
        'Non-Mature': '#FF9F43' # Laranja mais vibrante
    }
    
    # Plotar as barras empilhadas
    plt.bar(df['Country'], df['Number of Mature Nodes'],
            label='Mature Nodes', color=colors['Mature'],
            alpha=0.8, width=0.7)
    
    plt.bar(df['Country'], df['Number of Non-Mature Nodes'],
            bottom=df['Number of Mature Nodes'],
            label='Non-Mature Nodes', color=colors['Non-Mature'],
            alpha=0.8, width=0.7)
    
    # Adicionar valores em cada segmento
    for i in range(len(df)):
        # Valor para Mature
        mature_value = df['Number of Mature Nodes'].iloc[i]
        plt.text(i, mature_value/2, f'{int(mature_value):,}',
                ha='center', va='center',
                fontweight='bold', fontsize=10,
                color='white',
                bbox=dict(
                    facecolor='black',
                    alpha=0.7,
                    edgecolor='none',
                    pad=3,
                    boxstyle='round,pad=0.5'
                ))
        
        # Valor para Non-Mature
        non_mature_value = df['Number of Non-Mature Nodes'].iloc[i]
        plt.text(i, mature_value + non_mature_value/2,
                f'{int(non_mature_value):,}',
                ha='center', va='center',
                fontweight='bold', fontsize=10,
                color='white',
                bbox=dict(
                    facecolor='black',
                    alpha=0.7,
                    edgecolor='none',
                    pad=3,
                    boxstyle='round,pad=0.5'
                ))
        
        # Total no topo
        total = mature_value + non_mature_value
        plt.text(i, total + (total * 0.02),
                f'Total: {int(total):,}',
                ha='center', va='bottom',
                fontweight='bold', fontsize=12,
                color='white',
                bbox=dict(
                    facecolor='black',
                    alpha=0.7,
                    edgecolor='none',
                    pad=3,
                    boxstyle='round,pad=0.5'
                ))
    
    # Personalizar o gráfico com fundo no título
    plt.title('Distribuição de Mature/Non-Mature Nodes por País',
              fontsize=20, pad=20, fontweight='bold',
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=10,
                  boxstyle='round,pad=0.8'
              ))
    
    # Labels dos eixos com fundo
    plt.xlabel('País', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    plt.ylabel('Número de Nodes', 
              fontsize=14, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    # Adicionar grid suave
    plt.grid(True, axis='y', alpha=0.2, linestyle='--')
    
    # Personalizar a legenda com fundo
    legend = plt.legend(bbox_to_anchor=(1.05, 1), 
                       loc='upper left',
                       frameon=True, 
                       facecolor='black',
                       edgecolor='none', 
                       fontsize=12)
    legend.get_frame().set_alpha(0.7)
    
    # Ajustar os limites e rotação dos rótulos
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Remover as bordas
    sns.despine()
    
    # Ajustar o layout
    plt.tight_layout()
    
    # Guardar uma cópia da figura atual
    fig = plt.gcf()
    
    # Mostrar o gráfico
    plt.show()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook1', output_dir)
    save_plot(fig, 'mature_nodes_distribution', 'all_countries', folder, 'barplots')

## ================ Ficheiro 2 ================ ##

def plot_histogram(df, column_name, color, country, output_dir):
    # Verificações iniciais...
    if column_name not in df.columns:
        raise ValueError(f"A coluna '{column_name}' não existe no dataframe.")
    
    if df[column_name].nunique() == 1:
        raise ValueError(f"A coluna '{column_name}' tem valores constantes, o histograma pode não ser informativo.")

    # Configurar o tamanho da figura
    plt.figure(figsize=(10, 6))

    # Usar log scale no eixo X para distribuições muito enviesadas
    plt.hist(df[column_name], bins=50, color=color, edgecolor='black', alpha=0.7,
            density=True, log=True)
    plt.xscale('log')  # Escala logarítmica no eixo X
    

    # Configurar título e eixos
    plt.title(f'Distribuição de {column_name} para {country}', fontsize=16)
    plt.xlabel(f'{column_name} k', fontsize=14)
    plt.ylabel('Fração de nós com grau k', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Ajustar layout
    plt.tight_layout()

    # Salvar o gráfico
    folder = create_subfolder('NoteBook2', output_dir)
    hist_folder = create_subfolder('LogHistograms', folder)
    filename = f"LogHistogram_{column_name.replace(' ', '_')}_{country}.png"
    plt.savefig(hist_folder / filename, bbox_inches='tight', dpi=300)
    plt.show()


def plot_pie_chart(df, column_name, country, output_dir):
    """
    Cria um gráfico circular (donut chart) estilizado para visualizar a distribuição de uma variável categórica.
    """
    plt.figure(figsize=(10, 10))
    
    # Obter dados e ordenar por frequência
    data = df[column_name].value_counts()
    print(data)
    
    # Limitar a 10 categorias mais frequentes para melhor visualização
    if len(data) > 10:
        outros = pd.Series({'Outros': data[10:].sum()})
        data = pd.concat([data[:10], outros])
    
    # Cores personalizadas mais vibrantes
    colors = sns.color_palette('Set2', n_colors=len(data))
    
    # Criar o gráfico de rosca com sombra
    wedges, texts, autotexts = plt.pie(
        data,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={
            'width': 0.5,  # Largura da rosca
            'edgecolor': 'black',  # Borda branca
            'linewidth': 3,  # Espessura da borda
        },
        textprops={
            'fontsize': 11, 
            'weight': 'bold',
            'bbox': {
                'facecolor': 'black',
                'edgecolor': 'none',
                'alpha': 0.7,
                'pad': 3,
                'boxstyle': 'round,pad=0.3'
            }
        },
        pctdistance=0.85
    )
    
    # Estilizar as porcentagens
    plt.setp(autotexts, size=10, weight="bold", color="white",
             bbox=dict(facecolor='black', edgecolor='none', alpha=0.7, pad=3, boxstyle='round,pad=0.3'))
    
    # Adicionar título com estilo
    plt.title(f'Distribuição de {column_name}\n{country}', 
              fontsize=20, 
              pad=20, 
              fontweight='bold',
              bbox={
                  'facecolor': 'black',
                  'edgecolor': 'none',
                  'alpha': 0.7,
                  'pad': 10,
                  'boxstyle': 'round,pad=0.8'
              })
    
    # Adicionar valores absolutos no centro das fatias
    for wedge, value in zip(wedges, data):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.deg2rad(angle)) * 0.65  # Ajuste do raio
        y = np.sin(np.deg2rad(angle)) * 0.65
        
        # Adicionar valor com fundo
        plt.text(
            x, y, f'{value:,}',  # Formatar número com separador de milhares
            ha='center', 
            va='center',
            fontsize=10,
            fontweight='bold',
            color='white',
            bbox={
                'facecolor': 'black',
                'edgecolor': 'none',
                'alpha': 0.7,
                'pad': 3,
                'boxstyle': 'round,pad=0.3'
            }
        )
    
    # Adicionar círculo central para efeito visual
    centre_circle = plt.Circle((0, 0), 0.40, fc='black')
    plt.gca().add_artist(centre_circle)
    
    # Adicionar valor total no centro
    plt.text(0, 0, f'Total:\n{data.sum():,}',
             ha='center',
             va='center',
             fontsize=14,
             fontweight='bold')
    
    # Manter proporção circular
    plt.axis('equal')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook2', output_dir)
    piechart_folder = create_subfolder('PieCharts', folder)
    filename = f"PieChart_{column_name.replace(' ', '_')}_{country}.png"
    plt.savefig(piechart_folder / filename, 
                bbox_inches='tight',
                dpi=300,
                facecolor='white',
                edgecolor='none')
    
    plt.show()


def detect_power_law(data, column_name, country, output_dir):
    """
    Deteta e visualiza a lei de potência para uma determinada coluna de dados.
    
    Args:
        data (DataFrame): DataFrame com os dados
        column_name (str): Nome da coluna a analisar
        country (str): País dos dados
        output_dir (Path): Diretório base para salvar as imagens
    """
    # Ajustar os dados a uma lei de potência
    results = powerlaw.Fit(data[column_name], xmin=1)  # xmin define o limite inferior
    alpha = results.power_law.alpha  # Expoente da lei de potência
    xmin = results.power_law.xmin  # Valor mínimo usado no ajuste

    # Configurar a figura
    plt.figure(figsize=(10, 6))
    results.plot_pdf(color='b', linewidth=2, label="Dados Observados")
    results.power_law.plot_pdf(color='r', linestyle='--', label=f"Lei de Potência (α = {alpha:.2f})")
    
    # Configurar labels e título
    plt.xlabel(column_name, fontsize=14)
    plt.ylabel("Probabilidade", fontsize=14)
    plt.title(f"Distribuição e Ajuste de Lei de Potência para {column_name}", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Ajustar layout
    plt.tight_layout()

    # Criar diretórios necessários
    notebook2_folder = create_subfolder('NoteBook2', output_dir)
    powerlaw_folder = create_subfolder('PowerLaw', notebook2_folder)
    
    # Salvar o gráfico
    filename = f"PowerLaw_{column_name.replace(' ', '_')}_{country}.png"
    plt.savefig(powerlaw_folder / filename, bbox_inches='tight', dpi=300)
    
    # Mostrar o gráfico
    plt.show()

    # Retornar os resultados
    return alpha, xmin

def plot_community_distribution(df, column_name, community_column, country, output_dir):
    """
    Cria um gráfico de barras empilhadas mostrando a distribuição de uma coluna por comunidade.
    
    Args:
        df (DataFrame): DataFrame com os dados
        column_name (str): Nome da coluna a analisar ('game_name', 'mature', etc)
        community_column (str): Nome da coluna de comunidade ('louvain_community' ou 'lp_community')
        country (str): País dos dados
        output_dir (Path): Diretório para salvar as imagens
    """
    plt.figure(figsize=(15, 8))
    
    # Criar tabela de contingência
    cross_tab = pd.crosstab(df[community_column], df[column_name])
    
    # Se houver muitas categorias, pegar apenas as top N mais frequentes
    if cross_tab.shape[1] > 10:
        top_categories = df[column_name].value_counts().nlargest(10).index
        cross_tab = cross_tab[top_categories]
    
    # Plotar gráfico de barras empilhadas
    cross_tab.plot(kind='bar', stacked=True)
    
    plt.title(f'Distribuição de {column_name} por {community_column}\n{country}',
              fontsize=16, pad=20)
    plt.xlabel('Comunidade', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    
    # Rotacionar labels do eixo x
    plt.xticks(rotation=45, ha='right')
    
    # Ajustar legenda
    plt.legend(title=column_name, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adicionar grid
    plt.grid(True, alpha=0.3)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar o gráfico
    folder = create_subfolder('NoteBook2', output_dir)
    dist_folder = create_subfolder('CommunityDistribution', folder)
    filename = f"Distribution_{column_name}_{community_column}_{country}.png"
    plt.savefig(dist_folder / filename, 
                bbox_inches='tight',
                dpi=300)
    
    plt.show()

def plot_circular_distribution(df, country, output_dir):
    """
    Cria um círculo trigonométrico estilizado mostrando a distribuição temporal dos utilizadores.

    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
    """
    # Criar figura com fundo escuro
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='polar')

    # Configurar o grid circular
    ax.grid(True, alpha=0.2)

    # Plotar o círculo unitário
    circle = plt.Circle((0, 0), 1, fill=False, color='white', alpha=0.3, linestyle='--')
    ax.add_artist(circle)

    # Plotar os pontos com gradiente de cor baseado na data
    scatter = ax.scatter(df['normalized_day'],
                        np.ones(len(df)),
                        c=df['day_of_year'],
                        cmap='viridis',
                        alpha=0.6,
                        s=50)

    # Adicionar barra de cores
    cbar = plt.colorbar(scatter)
    cbar.set_label('Dia do Ano', fontsize=12)

    # Adicionar labels dos meses
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)

    # Ajustar a posição dos labels dos meses
    for angle, month in zip(angles, months):
        ax.text(angle, 1.2,
                month,
                ha='center',
                va='center',
                fontsize=12,
                fontweight='bold',
                bbox=dict(facecolor='black',
                            edgecolor='white',
                            alpha=0.7,
                            pad=3,
                            boxstyle='round,pad=0.5'))

    # Adicionar linhas para cada mês
    for angle in angles:
        ax.plot([angle, angle], [0, 1.1], 
                color='white',
                alpha=0.2,
                linestyle='--')

    # Configurar os limites e remover labels dos eixos
    ax.set_ylim(0, 1.3)
    ax.set_rticks([])

    # Adicionar título
    plt.title(f'Distribuição Circular de Criação de Contas - {country}',
                pad=20,
                fontsize=16,
                fontweight='bold',
                bbox=dict(facecolor='black',
                        edgecolor='white',
                        alpha=0.7,
                        pad=5,
                        boxstyle='round,pad=0.5'))

    # Adicionar anotações com estatísticas
    total_users = len(df)
    plt.figtext(0.02, 0.02,
                f'Total de utilizadores: {total_users:,}',
                fontsize=12,
                color='white',
                bbox=dict(facecolor='black',
                            edgecolor='white',
                            alpha=0.7,
                            pad=5,
                            boxstyle='round,pad=0.5'))

    # Criar pasta e salvar
    folder = create_subfolder('NoteBook2', output_dir)
    circular_folder = create_subfolder('CircularDistribution', folder)
    plt.savefig(circular_folder / f'circular_distribution_{country}.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='black',
                edgecolor='none')
    
    # Mostrar o gráfico
    plt.show()
    
    # Fechar a figura
    plt.close()

if __name__ == "__main__":
    # Escolher entre: DE, ENGB, ES, FR, PTBR, RU
    country = "PTBR"

    # Caminho do ficheiro CSV
    current_dir = Path.cwd()
    while current_dir.name != "Twitch":
        current_dir = current_dir.parent
    csv_path = current_dir / 'data' / country / f"twitch_network_metrics_{country}.csv"
    output_dir = current_dir / 'docs' / "Imagens"

    # Ler o ficheiro CSV
    df = pd.read_csv(csv_path)

    # Configuração de estilo dos gráficos
    plt.style.use('dark_background')
    sns.set_palette("colorblind")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12

    # Criar as subpastas para os tipos de gráficos
    hist_folder = create_subfolder('Histograms', output_dir)
    piechart_folder = create_subfolder('PieCharts', output_dir)

    # Histograma para variáveis contínuas
    plot_histogram(df,'degree', 'blue', country, output_dir, log_scale=False)  # Histograma para o grau (degree)
    plot_histogram(df,'degree_centrality', 'blue', country, output_dir, log_scale=False)
    plot_histogram(df,'closeness_centrality', 'green', country, output_dir, log_scale=False)
    plot_histogram(df,'betweenness_centrality', 'purple', country, output_dir, log_scale=False)
    plot_histogram(df,'eigenvector_centrality', 'red', country, output_dir, log_scale=False)
    plot_histogram(df,'views', 'orange', country, output_dir, log_scale=False)  # Histograma para views
    plot_histogram(df,'days', 'teal', country, output_dir, log_scale=False)  # Histograma para dias
    plot_histogram(df,'clustering_coef', 'pink', country, output_dir, log_scale=False) # Histograma para coeficiente de clustering

    # Gráficos circulares para variáveis categóricas
    plot_pie_chart(df, 'community_leiden', country, output_dir)
    plot_pie_chart(df, 'partner', country, output_dir)
    plot_pie_chart(df, 'mature', country, output_dir)

    alpha, xmin = detect_power_law(df, 'degree')
    print(f"Expoente (α): {alpha:.2f}")
    print(f"Valor mínimo (xmin): {xmin}")

    # Adicionar anotações com estatísticas
    total_users = len(df)
    plt.figtext(0.02, 0.02,
                f'Total de utilizadores: {total_users:,}',
                fontsize=12,
                color='white',
                bbox=dict(facecolor='black',
                            edgecolor='white',
                            alpha=0.7,
                            pad=5,
                            boxstyle='round,pad=0.5'))

    # Criar pasta e salvar
    folder = create_subfolder('NoteBook2', output_dir)
    circular_folder = create_subfolder('CircularDistribution', folder)
    plt.savefig(circular_folder / f'circular_distribution_{country}.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='black',
                edgecolor='none')
    
    # Mostrar o gráfico
    plt.show()
    
    # Fechar a figura
    plt.close()