from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
from pyspark.sql.functions import col, concat_ws
import os
import glob

# ============================================================
# Função auxiliar: remove arquivos .crc criados pelo Spark
# ============================================================
def cleanup_crc_files(path):
    for file in glob.glob(os.path.join(path, "*.crc")):
        try:
            os.remove(file)
        except:
            pass

            
# ============================================================
# Função para carregar e transformar o CSV em transações
# ============================================================
def generate_transaction_vector(spark, csv_path, selected_cols):
    """
    Lê o CSV e transforma as colunas selecionadas em listas de itens (transações).
    """
    df = spark.read.csv(csv_path, header=True, sep=";", inferSchema=False)

    # Filtra apenas colunas existentes no CSV
    cols = [c for c in selected_cols if c in df.columns]
    df = df.select(cols)

    # Converte cada linha em uma lista de itens válidos
    def row_to_list(row):
        return [
            f"{col}_{row[col].strip()}"
            for col in row.__fields__
            if row[col] and row[col].strip() != "" and row[col] != "97"
        ]

    df_rdd = df.rdd.map(lambda row: (row_to_list(row), ))
    df_transactions = spark.createDataFrame(df_rdd, ["items"])
    return df_transactions


# ============================================================
# Função para converter colunas do tipo array em string
# ============================================================
def convert_array_to_string(df, column):
    return df.withColumn(column, concat_ws(",", col(column)))


# ============================================================
# Função principal: executa FP-Growth para um grupo de colunas
# ============================================================
def process_temporal_group(spark, csv_path, group_name, selected_cols, year):
    print(f"\n=== Processing {group_name} (Year: {year}) ===")
    group_dir = f"results/temporal/{group_name}/{year}"
    os.makedirs(group_dir, exist_ok=True)

    # Cria as transações
    transactions = generate_transaction_vector(spark, csv_path, selected_cols)

    # Configura o FP-Growth com suporte/confiança de 1%
    fpGrowth = FPGrowth(itemsCol="items", minSupport=0.0, minConfidence=0.0)
    model = fpGrowth.fit(transactions)

    # =======================
    # Itens Frequentes
    # =======================
    print(f"[{group_name} - {year}] Processing frequent itemsets...")
    itemsets = model.freqItemsets
    itemsets_str = convert_array_to_string(itemsets, "items")

    # Salva resultados legíveis em .txt
    with open(f"{group_dir}/frequent_itemsets.txt", "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Frequent Itemsets - {group_name} ({year})\n")
        f.write("=" * 60 + "\n")
        for row in itemsets_str.collect():
            f.write(f"{row['items']:<150} | {row['freq']}\n")

    # Salva diretório CSV (com partes part-0000)
    csv_path_items = f"{group_dir}/frequent_itemsets_csv"
    itemsets_str.coalesce(1).write.option(
        "mapreduce.fileoutputcommitter.marksuccessfuljobs", "false"
    ).csv(csv_path_items, header=True, mode="overwrite")

    cleanup_crc_files(csv_path_items)

    # =======================
    # Regras de Associação
    # =======================
    print(f"[{group_name} - {year}] Processing association rules...")
    rules = model.associationRules
    rules_ante = convert_array_to_string(rules, "antecedent")
    rules_full = convert_array_to_string(rules_ante, "consequent")

    with open(f"{group_dir}/association_rules.txt", "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Association Rules - {group_name} ({year})\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Antecedent':<100} | {'Consequent':<30} | {'Confidence':<10} | {'Lift'}\n")
        f.write("-" * 180 + "\n")
        for row in rules_full.collect():
            ante = row["antecedent"]
            cons = row["consequent"]
            conf = f"{row['confidence']:.6f}"
            lift = f"{row['lift']:.6f}"
            f.write(f"{ante:<100} | {cons:<30} | {conf:<10} | {lift}\n")

    # Salva diretório CSV das regras
    csv_path_rules = f"{group_dir}/association_rules_csv"
    rules_full.coalesce(1).write.option(
        "mapreduce.fileoutputcommitter.marksuccessfuljobs", "false"
    ).csv(csv_path_rules, header=True, mode="overwrite")

    cleanup_crc_files(csv_path_rules)

    print(f"[{group_name} - {year}] Completed! Results saved in '{group_dir}'.")


# ============================================================
# Execução principal
# ============================================================
if __name__ == "__main__":
    # Cria a sessão Spark
    spark = SparkSession.builder \
        .appName("FP-Growth-Temporal-Analysis") \
        .config("spark.driver.memory", "8g") \
        .config("spark.driver.maxResultSize", "4g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

    os.makedirs("results/temporal", exist_ok=True)

    # ================================================
    # 🔹 Análise Temporal - Mesma pergunta em diferentes anos
    # ================================================
    TEMPORAL_GROUPS = {
        "P12_opiniao_machismo_2023": {
            "columns": ["P12"],
            "csv_path": "microdado/microdado_2023.csv",
            "year": 2023
        },
        "P05_opiniao_machismo_2021": {
            "columns": ["P05"],
            "csv_path": "microdado/microdado_2021.csv",
            "year": 2021
        },
        "P07_opiniao_machismo_2019": {
            "columns": ["P07"],
            "csv_path": "microdado/microdado_2019.csv",
            "year": 2019
        },
        "P07_opiniao_machismo_2017": {
            "columns": ["P07"],
            "csv_path": "microdado/microdado_2017.csv",
            "year": 2017
        },
    }

    # Processa cada grupo temporal
    for group_name, config in TEMPORAL_GROUPS.items():
        csv_path = config["csv_path"]
        columns = config["columns"]
        year = config["year"]
        
        # Verifica se o arquivo existe
        if os.path.exists(csv_path):
            process_temporal_group(spark, csv_path, group_name, columns, year)
        else:
            print(f"\nFile not found: {csv_path}")

    spark.stop()

    print("\nTemporal analysis completed for all groups!")
    print("Results organized in: results/temporal/")