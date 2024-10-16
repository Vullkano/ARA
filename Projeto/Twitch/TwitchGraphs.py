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
output_dir = current_dir / "Graph"

# Cria a pasta "Graph" se não existir
output_dir.mkdir(exist_ok=True)

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
def plot_histogram(column_name, title, color):
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
    plt.savefig(output_dir / f"{title.replace(' ', '_')}_{country}.png")
    plt.show()


# Histograma para variáveis contínuas
plot_histogram('degree', 'Histograma - Degree', 'blue')  # Histograma para o grau (degree)
plot_histogram('degree_centrality', 'Histograma - Degree Centrality', 'blue')
plot_histogram('closeness_centrality', 'Histograma - Closeness Centrality', 'green')
plot_histogram('betweenness_centrality', 'Histograma - Betweenness Centrality', 'purple')
plot_histogram('eigenvector_centrality', 'Histograma - Eigenvector Centrality', 'red')
plot_histogram('views', 'Histograma - Views', 'orange')  # Histograma para views
plot_histogram('days', 'Histograma - Days', 'teal')  # Histograma para dias
plot_histogram('clustering_coef', 'Histograma - Clustering Coefficient', 'pink')  # Histograma para coeficiente de clustering


# Função para desenhar e salvar um gráfico circular (pie chart)
def plot_pie_chart(column_name, title):
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
    plt.savefig(output_dir / f"{title.replace(' ', '_')}_{country}.png")
    plt.show()


# Gráficos circulares para variáveis categóricas
plot_pie_chart('community_leiden', 'Distribuição de Comunidades (Leiden)')
plot_pie_chart('partner', 'Distribuição de Parceiros (Partner)')
plot_pie_chart('mature', 'Distribuição de Conteúdo Maduro (Mature)')
