import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import powerlaw

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
    
    save_plot(fig, 'broadcaster_distribution', country, output_dir, 'Ficheiro0')

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
    
    save_plot(fig, 'game_categories', country, output_dir, 'Ficheiro0')

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
    
    # Criar o gráfico de barras
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
    
    save_plot(fig, 'null_distribution', country, output_dir, 'Ficheiro0')

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
    
    save_plot(fig, 'mature_content', country, output_dir, 'Ficheiro0')

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
# Função para criar subpastas para cada tipo de gráfico
def create_subfolder(folder_name, output_dir):
    subfolder = output_dir / folder_name
    subfolder.mkdir(exist_ok=True)
    return subfolder

# Função para desenhar e salvar um histograma
def plot_histogram(df, column_name, color, country, output_dir, log_scale=False):
    plt.figure(figsize=(10, 6))

    if log_scale:
        sns.histplot(df[column_name], kde=True, color=color, bins=30, edgecolor='black',
                     log_scale=(False, True))  # Escala logarítmica no eixo Y
    else:
        sns.histplot(df[column_name], kde=True, color=color, bins=30, edgecolor='black')  # Sem escala logarítmica

    plt.title(f'Histograma - {column_name} ({country})')
    plt.xlabel(column_name)
    plt.ylabel('Frequência')
    plt.grid(True)

    # Retira a notação científica apenas se a escala não for logarítmica
    if not log_scale:
        plt.ticklabel_format(style='plain', axis='y')

    # Adiciona linha média
    mean_value = df[column_name].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
    plt.text(mean_value + 0.5, 5, f'Média: {mean_value:.2f}', color='red')

    # Caminho para salvar o gráfico
    hist_folder = create_subfolder('Histograms', output_dir)
    filename = f"Histogram_{column_name.replace(' ', '_')}_{country}.png"
    plt.savefig(hist_folder / filename)
    plt.show()


# Função para desenhar e salvar um gráfico circular (pie chart)
def plot_pie_chart(df, column_name, country, output_dir):
    plt.figure(figsize=(8, 8))
    data = df[column_name].value_counts()
    # Gráfico de rosca
    wedges, texts, autotexts = plt.pie(
        data,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette('Paired'),
        wedgeprops={'width': 0.4}
    )

    plt.title(f'Donut Chart - {column_name} ({country})', fontsize=18)
    plt.axis('equal')  # Mantém a proporção circular

    # Adicionar anotações com o número total no centro das fatias
    for wedge, value in zip(wedges, data):
        angle = (wedge.theta2 + wedge.theta1) / 2  # Ângulo médio da fatia
        x = np.cos(np.deg2rad(angle)) * 0.7  # Ajuste do raio
        y = np.sin(np.deg2rad(angle)) * 0.7

        plt.text(
            x, y, str(value),
            color='black', fontsize=12, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor="white", alpha=0.8)
        )

    # Desativar o grid
    plt.grid(False)
    plt.gca().grid(False)

    # Caminho para salvar o gráfico
    piechart_folder = create_subfolder('PieCharts', output_dir)  # Cria subpasta "PieCharts"
    plt.savefig(piechart_folder / f"{'PieChart - {column_name} ({country})'.replace(' ', '_')}_{country}.png")
    plt.show()


def detect_power_law(data, column_name):
    # Ajustar os dados a uma lei de potência
    results = powerlaw.Fit(data[column_name], xmin=1)  # xmin define o limite inferior
    alpha = results.power_law.alpha  # Expoente da lei de potência
    xmin = results.power_law.xmin  # Valor mínimo usado no ajuste

    # Visualizar os dados e o ajuste
    plt.figure(figsize=(10, 6))
    results.plot_pdf(color='b', linewidth=2, label="Dados Observados")
    results.power_law.plot_pdf(color='r', linestyle='--', label=f"Lei de Potência (α = {alpha:.2f})")
    plt.xlabel(column_name)
    plt.ylabel("Probabilidade")
    plt.title(f"Distribuição e Ajuste de Lei de Potência para {column_name}")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Retornar os resultados
    return alpha, xmin

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