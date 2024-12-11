import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path
from scipy.stats import f_oneway
from scipy.stats import chi2_contingency
import matplotlib.patheffects as pe
import powerlaw

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
    
    # 5. V de Cramér e Coeficiente de Contingência de Pearson
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
                    
                    # Calcular Coeficiente de Contingência de Pearson
                    pearson_c = np.sqrt(chi2 / (chi2 + n))
                    
                    correlations['cramer'][(cat1, cat2)] = {
                        'cramer_v': cramer_v,
                        'pearson_c': pearson_c,
                        'p_value': p_value
                    }
                    
                except Exception as e:
                    print(f"Erro no cálculo para {cat1} e {cat2}: {str(e)}")
                    continue
    
    # Criar visualizações
    plot_correlations(correlations, country, output_dir)
    
    return correlations

def plot_correlations(correlations, country, output_dir):
    """
    Cria visualizações estilizadas para as diferentes correlações.
    """
    # Configurar estilo geral
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

    # Pearson e Spearman
    plt.figure(figsize=(15, 10))
    
    # Garantir que a diagonal é NaN
    pearson_matrix = correlations['pearson'].copy()
    spearman_matrix = correlations['spearman'].copy()
    np.fill_diagonal(pearson_matrix.values, np.nan)
    np.fill_diagonal(spearman_matrix.values, np.nan)
    
    # Criar máscaras para os triângulos
    mask_lower = np.triu(np.ones_like(pearson_matrix), k=1)
    mask_upper = np.tril(np.ones_like(spearman_matrix), k=-1)
    
    # Plot do triângulo inferior (Pearson)
    sns.heatmap(pearson_matrix,
                mask=mask_lower,
                annot=True,
                cmap='RdYlBu_r',
                vmin=-1,
                vmax=1,
                fmt='.2f',
                square=True,
                linewidths=1,
                cbar=True,
                cbar_kws={
                    "shrink": .8,
                    "label": "Coeficiente de Correlação",
                    "orientation": "vertical"
                },
                annot_kws={
                    "size": 8,
                    "color": "black"
                })
    
    # Plot do triângulo superior (Spearman)
    sns.heatmap(spearman_matrix,
                mask=mask_upper,
                annot=True,
                cmap='RdYlBu_r',
                vmin=-1,
                vmax=1,
                fmt='.2f',
                square=True,
                linewidths=1,
                cbar=False,
                annot_kws={
                    "size": 8,
                    "color": "black"
                })
    
    # Adicionar uma linha preta na diagonal
    for i in range(len(pearson_matrix)):
        plt.plot([i, i+1], [i, i+1], 'k-', linewidth=2)
    
    plt.title(f'Correlações de Pearson (inferior) e Spearman (superior)\n{country}',
              fontsize=16, pad=20, fontweight='bold',
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=10,
                  boxstyle='round,pad=0.8'
              ))
    
    # Rotacionar e alinhar os labels dos eixos
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Labels dos eixos com fundo preto
    plt.xlabel('Variáveis', 
              fontsize=12, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    plt.ylabel('Variáveis', 
              fontsize=12, labelpad=10,
              bbox=dict(
                  facecolor='black',
                  alpha=0.7,
                  edgecolor='none',
                  pad=5,
                  boxstyle='round,pad=0.5'
              ))
    
    plt.tight_layout()
    plt.savefig(pearson_dir / f'pearson_spearman_corr_{country}.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='black',
                edgecolor='none')
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
    
    # 4. V de Cramér e Coeficiente de Contingência
    if correlations['cramer']:
        plt.figure(figsize=(12, 8))
        
        # Criar matrizes para ambos os coeficientes
        cat_vars = sorted(list(set([cat for pair in correlations['cramer'].keys() for cat in pair])))
        cramer_matrix = pd.DataFrame(0.0, index=cat_vars, columns=cat_vars)
        contingency_matrix = pd.DataFrame(0.0, index=cat_vars, columns=cat_vars)
        
        for (cat1, cat2), values in correlations['cramer'].items():
            cramer_v = float(values['cramer_v'])
            pearson_c = float(values['pearson_c'])
            
            # Preencher matriz V de Cramér (triângulo inferior)
            cramer_matrix.loc[cat2, cat1] = cramer_v
            
            # Preencher matriz Coeficiente de Contingência (triângulo superior)
            contingency_matrix.loc[cat1, cat2] = pearson_c
        
        # Definir diagonal como NaN
        np.fill_diagonal(cramer_matrix.values, np.nan)
        np.fill_diagonal(contingency_matrix.values, np.nan)
        
        # Combinar as matrizes
        mask_lower = np.triu(np.ones_like(cramer_matrix), k=1)
        mask_upper = np.tril(np.ones_like(contingency_matrix), k=-1)
        
        # Plot do triângulo inferior (V de Cramér)
        sns.heatmap(cramer_matrix,
                    mask=mask_lower,
                    annot=True,
                    cmap='YlOrRd',
                    vmin=0,
                    vmax=1,
                    fmt='.2f',
                    square=True,
                    linewidths=1,
                    cbar_kws={
                        "shrink": .8,
                        "label": "Coeficiente"
                    },
                    annot_kws={
                        "size": 8,
                        "color": "black"
                    })
        
        # Plot do triângulo superior (Coeficiente de Contingência)
        sns.heatmap(contingency_matrix,
                    mask=mask_upper,
                    annot=True,
                    cmap='YlOrRd',
                    vmin=0,
                    vmax=1,
                    fmt='.2f',
                    square=True,
                    linewidths=1,
                    cbar=False,
                    annot_kws={
                        "size": 8,
                        "color": "black"
                    })
        
        # Adicionar uma linha preta na diagonal
        for i in range(len(cat_vars)):
            plt.plot([i, i+1], [i, i+1], 'k-', linewidth=2)
        
        plt.title(f'V de Cramér (inferior) e\nCoeficiente de Contingência (superior) - {country}',
                  fontsize=16, pad=20, fontweight='bold',
                  bbox=dict(
                      facecolor='black',
                      alpha=0.7,
                      edgecolor='none',
                      pad=10,
                      boxstyle='round,pad=0.8'
                  ))
        
        # Rotacionar e alinhar os labels dos eixos
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        # Labels dos eixos com fundo preto
        plt.xlabel('Variáveis', 
                  fontsize=12, labelpad=10,
                  bbox=dict(
                      facecolor='black',
                      alpha=0.7,
                      edgecolor='none',
                      pad=5,
                      boxstyle='round,pad=0.5'
                  ))
        
        plt.ylabel('Variáveis', 
                  fontsize=12, labelpad=10,
                  bbox=dict(
                      facecolor='black',
                      alpha=0.7,
                      edgecolor='none',
                      pad=5,
                      boxstyle='round,pad=0.5'
                  ))
        
        plt.tight_layout()
        plt.savefig(cramer_dir / f'cramer_contingency_corr_{country}.png',
                    dpi=300,
                    bbox_inches='tight',
                    facecolor='black',
                    edgecolor='none')
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