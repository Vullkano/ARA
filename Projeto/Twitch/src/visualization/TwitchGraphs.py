import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Função para criar subpastas para cada tipo de gráfico
def create_subfolder(folder_name, output_dir):
    subfolder = output_dir / folder_name
    subfolder.mkdir(exist_ok=True)
    return subfolder

# Função para desenhar e salvar um histograma
def plot_histogram(df, column_name, color, country, output_dir):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column_name], kde=True, color=color, bins=30, edgecolor='black')  # Adiciona contorno às barras
    plt.title(f'Histograma - {column_name} ({country})')
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
    hist_folder = create_subfolder('Histograms', output_dir)  # Cria subpasta "Histograms"
    plt.savefig(hist_folder / f"{'PieChart - {column_name} ({country})'.replace(' ', '_')}_{country}.png")
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
    plot_histogram(df,'degree', 'blue', country, output_dir)  # Histograma para o grau (degree)
    plot_histogram(df,'degree_centrality', 'blue', country, output_dir)
    plot_histogram(df,'closeness_centrality', 'green', country, output_dir)
    plot_histogram(df,'betweenness_centrality', 'purple', country, output_dir)
    plot_histogram(df,'eigenvector_centrality', 'red', country, output_dir)
    plot_histogram(df,'views', 'orange', country, output_dir)  # Histograma para views
    plot_histogram(df,'days', 'teal', country, output_dir)  # Histograma para dias
    plot_histogram(df,'clustering_coef', 'pink', country, output_dir) # Histograma para coeficiente de clustering

    # Gráficos circulares para variáveis categóricas
    plot_pie_chart(df, 'community_leiden', country, output_dir)
    plot_pie_chart(df, 'partner', country, output_dir)
    plot_pie_chart(df, 'mature', country, output_dir)