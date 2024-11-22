import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU
country = "PTBR"

# Caminho do ficheiro CSV
current_dir = Path.cwd()
csv_path = current_dir / country / f"twitch_network_metrics_{country}.csv"
output_dir = current_dir / "Graficos_Visualizacao"

# Cria a pasta "Graph" se não existir
output_dir.mkdir(exist_ok=True)

# Função para criar subpastas para cada tipo de gráfico
def create_subfolder(folder_name):
    subfolder = output_dir / folder_name
    subfolder.mkdir(exist_ok=True)
    return subfolder

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


# Função para desenhar e salvar um histograma
def plot_histogram(column_name, title, color, hist_folder):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column_name], kde=True, color=color, bins=30, edgecolor='black')  # Adiciona contorno às barras
    plt.title(f'{title} ({country})')
    plt.xlabel(column_name)
    plt.ylabel('Frequência')
    plt.grid(True)

    # Retira a notação científica
    plt.ticklabel_format(style='plain')

    # Adiciona linha média
    mean_value = df[column_name].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
    plt.text(mean_value + 0.5, 5, f'Média: {mean_value:.2f}', color='red')

    # Caminho para salvar o gráfico
    hist_folder = create_subfolder('Histograms')  # Cria subpasta "Histograms"
    plt.savefig(hist_folder / f"{title.replace(' ', '_')}_{country}.png")
    plt.show()


# Função para desenhar e salvar um gráfico circular (pie chart)
def plot_pie_chart(column_name, title, piechart_folder):
    plt.figure(figsize=(8, 8))
    data = df[column_name].value_counts()
    plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Paired'))
    plt.title(f'{title} ({country})', fontsize=18)
    plt.axis('equal')  # Equal aspect ratio to ensure the pie chart is circular

    # Retira a notação científica
    plt.ticklabel_format(style='plain')

    # Adicionar anotações com o número total
    for i, value in enumerate(data):
        plt.text(x=np.cos(np.deg2rad(i * 360 / len(data))) * 0.5,
                 y=np.sin(np.deg2rad(i * 360 / len(data))) * 0.5,
                 s=str(value), color='white', fontsize=12, ha='center')

    # Caminho para salvar o gráfico
    piechart_folder = create_subfolder('PieCharts')  # Cria subpasta "PieCharts"
    plt.savefig(piechart_folder / f"{title.replace(' ', '_')}_{country}.png")
    plt.show()


# Criar as subpastas para os tipos de gráficos
hist_folder = create_subfolder('Histograms')
piechart_folder = create_subfolder('PieCharts')

# Histograma para variáveis contínuas
plot_histogram('degree', 'Histograma - Degree', 'blue', hist_folder)  # Histograma para o grau (degree)
plot_histogram('degree_centrality', 'Histograma - Degree Centrality', 'blue', hist_folder)
plot_histogram('closeness_centrality', 'Histograma - Closeness Centrality', 'green', hist_folder)
plot_histogram('betweenness_centrality', 'Histograma - Betweenness Centrality', 'purple', hist_folder)
plot_histogram('eigenvector_centrality', 'Histograma - Eigenvector Centrality', 'red', hist_folder)
plot_histogram('views', 'Histograma - Views', 'orange', hist_folder)  # Histograma para views
plot_histogram('days', 'Histograma - Days', 'teal', hist_folder)  # Histograma para dias
plot_histogram('clustering_coef', 'Histograma - Clustering Coefficient', 'pink', hist_folder)  # Histograma para coeficiente de clustering

# Gráficos circulares para variáveis categóricas
plot_pie_chart('community_leiden', 'Distribuição de Comunidades (Leiden)', piechart_folder)
plot_pie_chart('partner', 'Distribuição de Parceiros (Partner)', piechart_folder)
plot_pie_chart('mature', 'Distribuição de Conteúdo Maduro (Mature)', piechart_folder)
