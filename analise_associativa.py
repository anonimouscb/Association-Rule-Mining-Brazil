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
def process_group(spark, csv_path, group_name, selected_cols):
    print(f"\n=== Processing {group_name} ===")
    group_dir = f"results/{group_name}"
    os.makedirs(group_dir, exist_ok=True)

    # Cria as transações
    transactions = generate_transaction_vector(spark, csv_path, selected_cols)

    # Configura o FP-Growth com suporte/confiança de 1%
    fpGrowth = FPGrowth(itemsCol="items", minSupport=0.01, minConfidence=0.01)
    model = fpGrowth.fit(transactions)

    # =======================
    # Itens Frequentes
    # =======================
    print(f"[{group_name}] Processing frequent itemsets...")
    itemsets = model.freqItemsets
    itemsets_str = convert_array_to_string(itemsets, "items")

    # Salva resultados legíveis em .txt
    with open(f"{group_dir}/frequent_itemsets.txt", "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Frequent Itemsets - {group_name}\n")
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
    print(f"[{group_name}] Processing association rules...")
    rules = model.associationRules
    rules_ante = convert_array_to_string(rules, "antecedent")
    rules_full = convert_array_to_string(rules_ante, "consequent")

    with open(f"{group_dir}/association_rules.txt", "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Association Rules - {group_name}\n")
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

    print(f"[{group_name}] Completed! Results saved in '{group_dir}'.")


# ============================================================
# Execução principal
# ============================================================
if __name__ == "__main__":
    # Cria a sessão Spark
    spark = SparkSession.builder \
        .appName("FP-Growth-DomesticViolence-MultiGroup") \
        .config("spark.driver.memory", "8g") \
        .config("spark.driver.maxResultSize", "4g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

    os.makedirs("results", exist_ok=True)

    # ================================================
    # 🔹 Grupos de colunas (exemplo)
    # ================================================
    GROUPS = {
        ## 1 - A visão das mulheres sobre desigualdade de gênero
        # Temporal "opiniao_machismo": ["P12"],
        "G1_opiniao_machismo": ["P12", "P08", "V13"],
        # Temporal "Mulheres são tratadas com respeito?" [P10]
        # Temporal "Onde são menos respeitadas?" [P11]
        "G2_violencia_aumentou_diminuiu_renda": ["P13","V14"],
        "G2_violencia_aumentou_diminuiu_raca": ["P13", "VD_RACA"],
        
        ## 2 - Percepção sobre a violência doméstica
        "G3_mulheres_denunciam?": ["P14"],
        # Temporal: Em sua opinião, as mulheres que sofrem agressão denunciam o fato às autoridades? ["P14"]
        "G4_motivo_nao_denunciar_renda":                    ["P14","V14"],
        "G4_motivo_nao_denunciar_medo":                     ["P14", "P15_15"],
        "G4_motivo_nao_denunciar_punicao":                  ["P14", "P15_16"],
        "G4_motivo_nao_denunciar_dependecia":               ["P14", "P15_17"],
        "G4_motivo_nao_denunciar_filhos":                   ["P14", "P15_18"],
        "G4_motivo_nao_denunciar_ultima_vez":               ["P14", "P15_19"],
        "G4_motivo_nao_denunciar_vergonha":                 ["P14", "P15_20"],
        "G4_motivo_nao_denunciar_ignorancia_direitros":     ["P14", "P15_21"],

        "G5_conhecida_sofreu_violencia":["P32"],
        "G5_conhecida_sofreu_violencia_fisica":["P32", "P33_33"],
        "G5_conhecida_sofreu_violencia_sexual":["P32", "P33_34"],
        "G5_conhecida_sofreu_violencia_psicologica":["P32", "P33_35"],
        "G5_conhecida_sofreu_violencia_patrimonial":["P32", "P33_36"],
        "G5_conhecida_sofreu_violencia_moral":["P32", "P33_37"],

        ## 3 - Os instrumentos de proteção às mulheres
        # Temporal "conhecimento_maria_da_penha":["P22"] 
        # Temporal "efetividade_maria_da_penha":["P23"]


        "G6_servicos_conhecidos_protecao":["P24_24", "P24_25", "P24_26", "P24_27", "P24_28", "P24_29"],
        "G6_conhecimento_medida_protetiva":["P31"],

        # 4 - A experiência de quem sofreu violência doméstica
        "G7_sofreu_violencia_por_homem":["P38","P39", "P40", "V14", "P41_41", "P41_42", "P41_43", "P41_44", "P41_45"],
        "G7_buscou_assistencia":["P46"],
        "G7_relacao_com_agressor":["VD_P49A", "P47", "P48", "VD_P50A", "VD_P51A", "P54"],
        "G7_estado_do_agressor":["P55_55", "P55_56", "P55_57", "P55_58", "P55_59", "P55B", "P55_60"],

        "G8_medidas_tomadas": [
        "P62",  # solicitou medida protetiva
        "P63",  # descumprimento da medida
        "P64_64", "P64_65", "P64_66", "P64_67", "P64_68", "P64_69", "P64_70", "P64_71"],  # atitudes após agressão (denunciar, procurar amigos, família, igreja, etc)
        
        "G9_avaliacao_servicos": ["P73_73", "P73_74", "P73_75"], # avaliação do atendimento em delegacias, central (liga 180)

        "G10_idade_primeira_agressao" : ["VD_P76"],

        "G11_ultimos_12_meses" :["P77_77", "P77_78", "P77_79", "P77_80", "P77_81", "P77_82", "P77_83"], 
        "G11_ainda_ultimos_12_meses" :["P84_84", "P84_85", "P84_86", "P84_87", "P84_88", "P84_89"], 
        
        "G12_":["P38", "P39", "P77_77", "P77_78", "P77_79", "P77_80", "P77_81", "P77_82", "P77_83", "P84_84", "P84_85", "P84_86", "P84_87", "P84_88", "P84_89" ],
        # COmparar o grupo acima com dados de 2021

        ## 4 - Perfil da entrevistadas
        "G13_moradore_no_domicilio": ["VD_P90"],
        "G13_numero_filhos": ["P92"],
        "G13_filhos_menores_idade": ["VD_P92A"],
        "G13_descricao_trabalho": ["V07"],
        "G13_tipo_servidora": ["V08"],
        "G13_carteira_assinada": ["V09"],
        "G13_trabalho_formal_informal": ["V10"],
        "G13_renda_proveniente": ["V12a"],
        "G13_renda_suficiente": ["V12B"],
        "G13_nivel_escolaridade": ["V03"],
        "G13_area_localizada": ["V05"],
        "G13_estado": ["P08"],
        "G13_regiao": ["VD_REGIAO"],
        "G13_porte": ["VD_PORTE"],
        "G13_idade": ["VD_IDADE"],
        "G13_raca": ["VD_RACA"],
        "G13_religiao": ["V13"],
        "G13_renda_total_inclusa": ["V14"],
        "G_new1_religiao_x_busca_ajuda": ["V13","P46","P64_64","P64_65","P64_66"],
        "G_new2_escolaridade_x_confianca_institucional": ["V03","P14","P23"],
        "G_new3_renda_x_tipo_violencia_conhecida": ["V14","P32","P33_33","P33_35","P33_36"],

        ## Novos grupos — não analisados na pesquisa do PDF
        "G_new4_regiao_x_conhecimento_maria_penha":     ["VD_REGIAO", "P22"],
        "G_new5_idade_x_percepcao_violencia_aumentou":  ["VD_IDADE", "P13"],
        "G_new6_renda_x_busca_assistencia_saude":       ["V14", "P46"],
        "G_new7_idade_x_medida_protetiva":              ["VD_IDADE", "P62"],
        "G_new8_regiao_x_vitimizacao":                  ["VD_REGIAO", "P38"],

    }

    # Caminho do CSV
    CSV_PATH = "microdado/microdado_2023.csv"

    # Processa cada grupo
    for group_name, columns in GROUPS.items():
        process_group(spark, CSV_PATH, group_name, columns)

    spark.stop()

    print("\nAnalysis completed for all groups!")
