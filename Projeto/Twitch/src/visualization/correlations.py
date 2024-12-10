import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path
from scipy.stats import f_oneway
from scipy.stats import chi2_contingency

def calculate_correlations(df, country, output_dir):
    """
    Calcula diferentes tipos de correlações baseado no tipo de variáveis.
    
    Args:
        df (DataFrame): DataFrame com os dados
        country (str): País sendo analisado
        output_dir (Path): Diretório para salvar as imagens
    """
    # Separar variáveis por tipo
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'bool', 'category']).columns
    
    # Dicionário para armazenar resultados
    correlations = {
        'pearson': None,
        'spearman': None,
        'eta': {},
        'cramer': {}
    }
    
    # 1. Correlação de Pearson (variáveis numéricas)
    correlations['pearson'] = df[numeric_cols].corr(method='pearson')
    
    # 2. Correlação de Spearman (variáveis numéricas, não assume linearidade)
    correlations['spearman'] = df[numeric_cols].corr(method='spearman')
    
    # 3. Correlação ETA (entre variáveis categóricas e numéricas)
    for cat_col in categorical_cols:
        for num_col in numeric_cols:
            try:
                # Verificar se há valores válidos
                if df[cat_col].isna().all() or df[num_col].isna().all():
                    continue
                    
                # Remover valores NA
                valid_data = df[[cat_col, num_col]].dropna()
                if len(valid_data) == 0:
                    continue
                
                categories = valid_data[cat_col].unique()
                if len(categories) <= 1:  # Precisa ter mais de uma categoria
                    continue
                
                # Calcular ETA
                categories_means = valid_data.groupby(cat_col, observed=True)[num_col].mean()
                grand_mean = valid_data[num_col].mean()
                
                numerator = sum(len(valid_data[valid_data[cat_col] == cat]) * 
                              (categories_means[cat] - grand_mean)**2 
                              for cat in categories)
                denominator = sum((valid_data[num_col] - grand_mean)**2)
                
                if denominator > 0:
                    eta = np.sqrt(numerator/denominator)
                    correlations['eta'][(cat_col, num_col)] = eta
            except Exception as e:
                print(f"Erro no cálculo ETA para {cat_col} e {num_col}: {str(e)}")
                continue
    
    # 5. V de Cramér (entre variáveis categóricas)
    for cat1 in categorical_cols:
        for cat2 in categorical_cols:
            if cat1 < cat2:  # Evita calcular correlações duplicadas
                try:
                    # Criar tabela de contingência
                    contingency = pd.crosstab(df[cat1], df[cat2])
                    
                    # Calcular chi-quadrado
                    chi2, p_value, dof, expected = chi2_contingency(contingency)
                    
                    # Calcular V de Cramér
                    n = len(df)
                    min_dim = min(len(df[cat1].unique()), len(df[cat2].unique())) - 1
                    cramer_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
                    
                    correlations['cramer'][(cat1, cat2)] = {
                        'cramer_v': cramer_v,
                        'p_value': p_value
                    }
                    
                except Exception as e:
                    print(f"Erro no cálculo V de Cramér para {cat1} e {cat2}: {str(e)}")
                    continue
    
    # Criar visualizações
    plot_correlations(correlations, country, output_dir)
    
    return correlations

def plot_correlations(correlations, country, output_dir):
    """
    Cria visualizações estilizadas para as diferentes correlações.
    """
    # Configurar estilo
    plt.style.use('dark_background')
    
    # Criar pastas
    notebook3_dir = output_dir / 'NoteBook3'
    notebook3_dir.mkdir(exist_ok=True)
    
    pearson_dir = notebook3_dir / 'Pearson'
    spearman_dir = notebook3_dir / 'Spearman'
    eta_dir = notebook3_dir / 'ETA'
    cramer_dir = notebook3_dir / 'Cramer'
    
    for dir_path in [pearson_dir, spearman_dir, eta_dir, cramer_dir]:
        dir_path.mkdir(exist_ok=True)
    
    # 1. Heatmap para Pearson
    plt.figure(figsize=(15, 10))
    
    # Criar máscaras para triangulos superior e inferior
    mask_lower = np.tril(np.ones_like(correlations['pearson']))
    mask_upper = np.triu(np.ones_like(correlations['pearson']), k=1)
    
    # Plot do triângulo inferior com heatmap
    sns.heatmap(correlations['pearson'],
                mask=mask_upper,
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8},
                annot_kws={"size": 8})
    
    # Plot do triângulo superior com padrão
    ax = plt.gca()
    for i in range(len(correlations['pearson'])):
        for j in range(i+1, len(correlations['pearson'])):
            ax.add_patch(plt.Rectangle((i, j), 1, 1, 
                                     fill=True,
                                     facecolor='gray',
                                     alpha=0.5))
    
    plt.title(f'Correlação de Pearson - {country}', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(pearson_dir / f'pearson_corr_{country}.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 2. Heatmap para Spearman
    plt.figure(figsize=(15, 10))
    
    # Plot do triângulo inferior com heatmap
    sns.heatmap(correlations['spearman'],
                mask=mask_upper,
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                square=True,
                linewidths=1,
                cbar_kws={"shrink": .8},
                annot_kws={"size": 8})
    
    # Plot do triângulo superior com padrão diferente
    ax = plt.gca()
    for i in range(len(correlations['spearman'])):
        for j in range(i+1, len(correlations['spearman'])):
            ax.add_patch(plt.Rectangle((i, j), 1, 1, 
                                     fill=True,
                                     facecolor='gray',
                                     alpha=0.5))
    
    plt.title(f'Correlação de Spearman - {country}', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(spearman_dir / f'spearman_corr_{country}.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 3. Barplot para ETA com melhor visualização
    plt.figure(figsize=(15, 8))
    eta_df = pd.DataFrame(list(correlations['eta'].items()), 
                         columns=['pairs', 'correlation'])
    eta_df[['categorical', 'numerical']] = pd.DataFrame(eta_df['pairs'].tolist())
    
    # Agrupar por variável numérica (invertido)
    grouped_eta = eta_df.groupby('numerical')
    
    # Preparar o plot
    categories = eta_df['categorical'].unique()
    x = np.arange(len(categories))
    width = 0.8 / len(grouped_eta)
    
    # Criar barplot agrupado
    for i, (num, group) in enumerate(grouped_eta):
        # Reorganizar dados para manter ordem consistente
        values = [group[group['categorical'] == cat]['correlation'].iloc[0] 
                 if not group[group['categorical'] == cat].empty 
                 else 0 
                 for cat in categories]
        
        # Calcular posição das barras
        pos = x + (i - len(grouped_eta)/2 + 0.5) * width
        
        # Criar barras
        bars = plt.bar(pos, values,
                      width=width,
                      label=num,
                      alpha=0.7)
        
        # Adicionar rótulos nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Só mostrar rótulo se houver valor
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom',
                        fontsize=8)
    
    # Configurar eixos e legendas
    plt.title(f'Correlações ETA - {country}', fontsize=16, pad=20)
    plt.xlabel('Variáveis Categóricas', fontsize=12)
    plt.ylabel('Valor ETA', fontsize=12)
    
    # Ajustar labels do eixo X
    plt.xticks(x, categories, rotation=45, ha='right')
    
    # Ajustar legenda
    plt.legend(title='Variáveis Numéricas', 
              bbox_to_anchor=(1.05, 1), 
              loc='upper left',
              title_fontsize=10)
    
    # Adicionar grid e ajustar layout
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    
    # Salvar e mostrar
    plt.savefig(eta_dir / f'eta_corr_{country}.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 4. V de Cramér
    if correlations['cramer']:
        plt.figure(figsize=(12, 8))
        
        # Criar matriz de correlação para V de Cramér
        cat_vars = sorted(list(set([cat for pair in correlations['cramer'].keys() for cat in pair])))
        cramer_matrix = pd.DataFrame(0.0, index=cat_vars, columns=cat_vars)
        
        for (cat1, cat2), values in correlations['cramer'].items():
            cramer_matrix.loc[cat1, cat2] = float(values['cramer_v'])
            cramer_matrix.loc[cat2, cat1] = float(values['cramer_v'])
        
        # Mascarar triângulo superior
        mask = np.triu(np.ones_like(cramer_matrix), k=0)
        
        # Plot heatmap
        sns.heatmap(cramer_matrix,
                    mask=mask,
                    annot=True,
                    cmap='YlOrRd',
                    vmin=0,
                    vmax=1,
                    fmt='.2f',
                    square=True,
                    linewidths=1,
                    cbar_kws={"shrink": .8},
                    annot_kws={"size": 8})
        
        plt.title(f'Correlações V de Cramér - {country}', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig(cramer_dir / f'cramer_corr_{country}.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()


# Exemplo de uso
if __name__ == "__main__":
    # Configurar diretórios
    current_dir = Path.cwd()
    country = "PTBR"  # ou outro país
    
    # Carregar dados
    csv_path = current_dir / 'data' / country / f"twitch_network_metrics_{country}.csv"
    output_dir = current_dir / 'docs' / "Imagens" / 'Correlations'
    output_dir.mkdir(exist_ok=True)
    
    # Ler dados
    df = pd.read_csv(csv_path)
    
    # Calcular correlações
    correlations = calculate_correlations(df, country, output_dir)