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
        transparent=True  # Adicionar esta linha para manter o fundo transparente
    )
    plt.close(fig)

## ================ Ficheiro 1 ================ ##

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
    Cria um círculo trigonométrico estilizado mostrando a distribuição temporal dos usuários.

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
                f'Total de Usuários: {total_users:,}',
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