import pandas as pd
import sys

# ============================================================
# Variáveis configuráveis
# ============================================================
CSV_FILE = 'microdado/microdado_2023.csv'
COLUMN_NAME = 'P12'

# ============================================================
# Função para analisar uma coluna
# ============================================================
def analyze_column(csv_path, column):
    try:
        df = pd.read_csv(csv_path, sep=';')
        
        if column not in df.columns:
            print(f"❌ Erro: Coluna '{column}' não encontrada no arquivo!")
            print(f"Colunas disponíveis: {df.columns.tolist()}")
            return
        
        # Contar quantas respostas existem (não nulas) na pergunta
        total_respostas = df[column].notna().sum()
        total_registros = len(df)
        valores_ausentes = df[column].isna().sum()
        
        print("=" * 60)
        print(f"Análise da Pergunta {column} - {csv_path}")
        print("=" * 60)
        print(f"Total de registros: {total_registros}")
        print(f"Total de respostas (não nulas): {total_respostas}")
        print(f"Valores ausentes/nulos: {valores_ausentes}")
        print(f"Taxa de resposta: {(total_respostas/total_registros)*100:.2f}%")
        print("\nDistribuição de respostas:")
        distribuicao = df[column].value_counts().sort_index().rename("Quantidade")
        distribuicao = distribuicao.to_frame()
        distribuicao["Porcentagem"] = (distribuicao["Quantidade"] / total_respostas) * 100
        print(distribuicao.to_string(formatters={"Porcentagem": lambda x: f"{x:.2f}%"}))
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{csv_path}' não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")

# ============================================================
# Execução
# ============================================================
if __name__ == "__main__":
    # Se argumentos forem passados pela linha de comando
    if len(sys.argv) >= 2:
        column = sys.argv[1]
    else:
        column = COLUMN_NAME
    
    if len(sys.argv) >= 3:
        csv_file = sys.argv[2]
    else:
        csv_file = CSV_FILE
    
    analyze_column(csv_file, column)
