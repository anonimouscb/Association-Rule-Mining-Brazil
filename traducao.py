import pandas as pd

def criar_dicionario_pesquisa(arquivo_excel, incluir_pergunta=True):
    """
    Cria um dicionário a partir de dados de pesquisa estruturados em Excel.
    
    Args:
        arquivo_excel (str): Caminho para o arquivo Excel
        incluir_pergunta (bool): Se True, inclui a pergunta na descrição
    
    Returns:
        dict: Dicionário com chaves no formato "P_XX_YY" e valores descritivos
    """
    
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo_excel)
    
    # Renomear colunas para facilitar o acesso
    df.columns = ['codigo_variavel', 'descricao_variavel', 'codigo_categoria', 'descricao_categoria']
    
    # Remover linhas vazias e com códigos de categoria vazios
    df = df.dropna(subset=['codigo_categoria'])
    df = df[df['codigo_categoria'] != '-']
    
    dicionario_resultado = {}
    pergunta_atual = None
    descricao_pergunta_atual = None
    
    for index, row in df.iterrows():
        codigo_variavel = row['codigo_variavel']
        descricao_variavel = row['descricao_variavel']
        codigo_categoria = row['codigo_categoria']
        descricao_categoria = row['descricao_categoria']
        
        # Se há um novo código de variável (não vazio), atualize a pergunta atual
        if pd.notna(codigo_variavel) and codigo_variavel.strip():
            pergunta_atual = codigo_variavel.strip()
            if pd.notna(descricao_variavel):
                # Limpar a descrição da pergunta
                descricao_pergunta_atual = limpar_descricao_pergunta(descricao_variavel.strip())
        
        # Se temos pergunta atual e categoria válida, criar entrada no dicionário
        if pergunta_atual and pd.notna(codigo_categoria) and pd.notna(descricao_categoria):
            # Limpar o código da pergunta (remover pontos, espaços extras)
            codigo_limpo = pergunta_atual.replace('.', '').strip()
            
            # Criar a chave do dicionário
            chave = f"{codigo_limpo}_{int(float(codigo_categoria))}"
            
            # Criar o valor
            if incluir_pergunta and descricao_pergunta_atual:
                valor = f"{descricao_categoria.strip()} ({descricao_pergunta_atual})"
            else:
                valor = descricao_categoria.strip()
            
            dicionario_resultado[chave] = valor
    
    return dicionario_resultado

def limpar_descricao_pergunta(descricao):
    """
    Remove instruções de pesquisa desnecessárias da descrição da pergunta.
    """
    if not descricao:
        return descricao
    
    import re
    
    # Primeiro, remover qualquer texto que contenha "Resposta" até o final da frase
    descricao_limpa = re.sub(r'.*Resposta.*', '', descricao, flags=re.IGNORECASE)
    
    # Lista de padrões específicos a serem removidos
    padroes_remover = [
        "Ler as alternativas",
        "NÃO Ler Alternativas",
        "Não ler:",
        "Vou começar a pesquisa.",
        "LER perguntas",
        "ALTERNAR perguntas",
        "ler opções de respostas",
        "NÃO alternar respostas",
        "Qual?",
        "(Não ler)",
        "Ler as alternativas"
    ]
    
    # Remover cada padrão
    for padrao in padroes_remover:
        descricao_limpa = descricao_limpa.replace(padrao, "")
    
    # Remover caracteres e pontuações extras
    descricao_limpa = descricao_limpa.replace("()", "")
    descricao_limpa = descricao_limpa.replace("/ / / /)", "")
    descricao_limpa = descricao_limpa.replace("/ /", "")
    descricao_limpa = descricao_limpa.replace("//", "")
    descricao_limpa = descricao_limpa.replace("  ", " ")
    descricao_limpa = descricao_limpa.strip()
    
    # Remover pontos extras no final
    while descricao_limpa.endswith('.') and descricao_limpa.count('.') > 1:
        descricao_limpa = descricao_limpa[:-1].strip()
    
    # Remover parênteses vazios que sobraram
    descricao_limpa = re.sub(r'\(\s*\)', '', descricao_limpa)
    
    # Limpar espaços extras novamente
    descricao_limpa = re.sub(r'\s+', ' ', descricao_limpa).strip()
    
    return descricao_limpa

def processar_dados_texto(texto_dados, incluir_pergunta=True):
    """
    Processa dados em formato texto (como o exemplo fornecido).
    
    Args:
        texto_dados (str): Dados em formato de texto
        incluir_pergunta (bool): Se True, inclui a pergunta na descrição
    
    Returns:
        dict: Dicionário com chaves no formato "P_XX_YY" e valores descritivos
    """
    
    linhas = texto_dados.strip().split('\n')
    dicionario_resultado = {}
    pergunta_atual = None
    descricao_pergunta_atual = None
    
    for linha in linhas[1:]:  # Pular o cabeçalho
        if not linha.strip():
            continue
            
        # Dividir por tabulação
        partes = linha.split('\t')
        
        if len(partes) >= 4:
            codigo_variavel = partes[0].strip()
            descricao_variavel = partes[1].strip()
            codigo_categoria = partes[2].strip()
            descricao_categoria = partes[3].strip()
            
            # Se há um novo código de variável (não vazio), atualize a pergunta atual
            if codigo_variavel and codigo_variavel != '-':
                pergunta_atual = codigo_variavel
                if descricao_variavel and descricao_variavel != '-':
                    # Limpar a descrição da pergunta
                    descricao_pergunta_atual = limpar_descricao_pergunta(descricao_variavel)
            
            # Se temos pergunta atual e categoria válida, criar entrada no dicionário
            if (pergunta_atual and codigo_categoria and codigo_categoria != '-' 
                and descricao_categoria and descricao_categoria != '-'):
                
                # Limpar o código da pergunta
                codigo_limpo = pergunta_atual.replace('.', '').strip()
                
                # Criar a chave do dicionário
                try:
                    chave = f"{codigo_limpo}_{int(float(codigo_categoria))}"
                    
                    # Criar o valor
                    if incluir_pergunta and descricao_pergunta_atual:
                        valor = f"{descricao_categoria} ({descricao_pergunta_atual})"
                    else:
                        valor = descricao_categoria
                    
                    dicionario_resultado[chave] = valor
                except ValueError:
                    # Pular se não conseguir converter código_categoria para número
                    continue
    
    return dicionario_resultado

# Processar os dados de exemplo
dicionario = criar_dicionario_pesquisa('microdado_completo_violência_doméstica_e_familiar_contra_a_mulher/Dicionario - 2023.xlsx', incluir_pergunta=True)

print("Dicionário gerado:")
# print("=" * 50)
for i in dicionario:
    print(f"{i} : {dicionario[i]}")
