import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import pathlib

def get_correlations(country:str, current_dir:pathlib.WindowsPath = Path.cwd()):
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    assert country in countries
    assert type(current_dir) == pathlib.WindowsPath and "Twitch" in str(current_dir)
    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    csv_path = current_dir / 'data' / country / f"twitch_network_metrics_{country}.csv"
    output_dir = current_dir / 'docs' / "Imagens" / 'CorrPlot'

    # Criar a pasta "Imagens" se não existir
    output_dir.mkdir(exist_ok=True)

    # Ler o ficheiro CSV
    df = pd.read_csv(csv_path)

    # Converter as variáveis booleanas para inteiros
    df['partner'] = df['partner'].astype(int)
    df['mature'] = df['mature'].astype(int)

    # Excluir a coluna "node" da matriz de correlação
    df = df.drop(columns=['node'])

    # Calcular a matriz de correlação (Pearson)
    correlation_matrix = df.corr(method='pearson')

    # Configurar o tamanho da figura
    plt.figure(figsize=(14, 10))

    # Definir o fundo escuro para a visualização
    plt.style.use('dark_background')

    # Criar o mapa de calor para a correlação
    sns.heatmap(correlation_matrix,
                annot=True,
                fmt=".2f",
                cmap='Spectral_r',  # Paleta de cores mais vibrante
                square=True,
                cbar_kws={"shrink": .8, 'ticks': np.round(np.linspace(-1, 1, 5), 2)},  # Ajuste na barra de cor
                linewidths=0.5,
                linecolor='gray',
                annot_kws={"fontsize": 10, "weight": "bold", "color": "black"},  # Letra mais bold e cor distinta
                alpha=0.9,  # Um pouco de transparência para melhorar a estética
                vmin=-1,  # Definir limite inferior da escala
                vmax=1)    # Definir limite superior da escala

    # Configurar os rótulos e título
    plt.title('Matriz de Correlação', fontsize=22, pad=20, color='white', weight='bold')
    plt.xticks(rotation=90, fontsize=12, color='white')
    plt.yticks(rotation=0, fontsize=12, color='white')

    # Ajustar layout
    plt.tight_layout()

    # Caminho para salvar a imagem
    output_path = output_dir / f"matriz_correlacao_{country}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')  # Melhor qualidade da imagem

    # Mostrar o gráfico
    plt.show()

    print(f"Imagem salva em: {output_path}")


if __name__ == "__main__":
    # Escolher entre: DE, ENGB, ES, FR, PTBR, RU
    country = "ENGB"

    get_correlations(country)