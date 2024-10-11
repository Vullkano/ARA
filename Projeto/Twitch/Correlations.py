import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Escolher entre: DE, ENGB, ES, FR, PTBR, RU
country = "PTBR"

# Caminho do ficheiro CSV
current_dir = Path.cwd()
csv_path = current_dir / country / f"twitch_network_metrics_{country}.csv"

# Ler o ficheiro CSV
df = pd.read_csv(csv_path)

# Converter as variáveis booleanas para inteiros
df['partner'] = df['partner'].astype(int)
df['mature'] = df['mature'].astype(int)

# Calcular a matriz de correlação
correlation_matrix = df.corr()

# Configurar o tamanho da figura
plt.figure(figsize=(12, 8))

# Criar o mapa de calor
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})

# Configurar os rótulos e título
plt.title('Matriz de Correlação das Variáveis')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# Mostrar o gráfico
plt.tight_layout()
plt.show()
