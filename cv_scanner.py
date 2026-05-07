#!/usr/bin/env python3
import sys
import re
import csv
import os
from datetime import datetime

# Configuração da Base Analítica (CSV)
CSV_FILE = "cv_analytics.csv"

# Vetores Principais (Pontuação)
VETORES = {
    "TIER_1_CLOUD": {
        "peso": 3,
        "palavras": [
            r"\baws\b", r"\blinux\b", r"\bshell\b", r"\bpython\b", r"\bterraform\b",
            r"\bserverless\b", r"\bfinops\b", r"\bdocker\b", r"\bec2\b", r"\brds\b",
            r"\bcloud\b", r"\bdevops\b", r"\bci/cd\b", r"\bia\b", r"\bllm\b"
        ],
        "nome": "🚀 Tier 1 (Cloud & Automação)"
    },
    "TIER_2_SYSTEMS": {
        "peso": 2,
        "palavras": [
            r"\bapi[s]?\b", r"\brest\b", r"\bsql\b", r"\bbanco de dados\b", r"\bpostman\b",
            r"\bwebhook[s]?\b", r"\blog[s]?\b", r"\bintegraç[ãa]o\b", r"\bintegraçõ[e]?s\b", 
            r"\brequisitos\b", r"\bswagger\b", r"\bitsm\b", r"\bjson\b", r"\bbackend\b"
        ],
        "nome": "🛡️ Tier 2 (Sustentação & Backend)"
    },
    "TIER_3_DRAINERS": {
        "peso": -3,
        "palavras": [
            r"\bfigma\b", r"\bangular\b", r"\breact\b", r"\bux\b", r"\bui\b",
            r"\bfront-end\b", r"\bfrontend\b", r"\bcss\b", r"\bhtml\b", 
            r"\bprotótipo[s]?\b", r"\btelas\b"
        ],
        "nome": "⚠️ Tier 3 (Red Flags / Front-end / UX)"
    }
}

# Vetores Secundários (Apenas Coleta de Dados Analíticos, sem pontuação)
VETORES_SECUNDARIOS = {
    "SENIORIDADE": [r"\bj[úu]nior\b", r"\bpleno\b", r"\bs[êe]nior\b", r"\bespecialista\b", r"\btech lead\b"],
    "METODOLOGIA": [r"\bagile\b", r"\bscrum\b", r"\bkanban\b", r"\bitil\b"],
    "MODELO_TRABALHO": [r"\bremoto\b", r"\bhome office\b", r"\bh[íi]brido\b", r"\bpresencial\b"]
}

# Cores
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
CYAN = "\033[96m"

def save_to_csv(data_dict):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Cabeçalho se o arquivo não existir
        if not file_exists:
            writer.writerow(['Data', 'Arquivo', 'Score_Total', 'Score_Cloud', 'Score_Systems', 'Score_Drainers', 'Veredicto', 'Senioridade', 'Metodologia', 'Modelo', 'Termos_Encontrados'])
        
        # Consolida todas as palavras encontradas para a coluna de termos
        todos_termos = f"{data_dict['termos_cloud']} | {data_dict['termos_sys']} | {data_dict['termos_drain']}"
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data_dict['arquivo'],
            data_dict['score_total'],
            data_dict['score_cloud'],
            data_dict['score_sys'],
            data_dict['score_drain'],
            data_dict['veredicto'],
            data_dict['sec_senioridade'],
            data_dict['sec_metodologia'],
            data_dict['sec_modelo'],
            todos_termos
        ])

def analyze_job(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"{RED}Erro: Arquivo '{file_path}' não encontrado.{RESET}")
        sys.exit(1)

    resultados = {
        "TIER_1_CLOUD": {"pontos": 0, "encontradas": {}},
        "TIER_2_SYSTEMS": {"pontos": 0, "encontradas": {}},
        "TIER_3_DRAINERS": {"pontos": 0, "encontradas": {}}
    }
    
    secundarios_encontrados = {k: [] for k in VETORES_SECUNDARIOS.keys()}
    pontuacao_total = 0

    # Varredura Principal (Com Frequência)
    for categoria, info in VETORES.items():
        peso = info["peso"]
        for padrao in info["palavras"]:
            matches = re.findall(padrao, text)
            qtd = len(matches)
            if qtd > 0:
                palavra_limpa = padrao.replace(r"\b", "").replace(r"[s]?", "").replace(r"[ãa]", "a").replace(r"çõ[e]?s", "coes").replace(r"[úu]", "u").replace(r"[êe]", "e").replace(r"[íi]", "i")
                resultados[categoria]["encontradas"][palavra_limpa] = qtd
                # A pontuação ainda é somada uma vez por palavra para evitar distorção, mas a frequência é guardada
                pontuacao_total += peso
                resultados[categoria]["pontos"] += peso

    # Varredura Secundária
    for categoria, padroes in VETORES_SECUNDARIOS.items():
        for padrao in padroes:
            if re.search(padrao, text):
                palavra_limpa = padrao.replace(r"\b", "").replace(r"[s]?", "").replace(r"[ãa]", "a").replace(r"çõ[e]?s", "coes").replace(r"[úu]", "u").replace(r"[êe]", "e").replace(r"[íi]", "i")
                secundarios_encontrados[categoria].append(palavra_limpa)

    # Regras de Classificação
    pts_cloud = resultados["TIER_1_CLOUD"]["pontos"]
    pts_sys = resultados["TIER_2_SYSTEMS"]["pontos"]
    pts_drain = resultados["TIER_3_DRAINERS"]["pontos"]

    veredicto = ""
    cor_veredicto = RESET

    if pts_drain <= -6:
        veredicto = "TIER 3 (Evitar) - Vaga fortemente inclinada a Front-end/UX."
        cor_veredicto = RED
    elif pts_cloud >= 6 and pts_cloud >= pts_sys:
        veredicto = "TIER 1 (The Dream) - Vaga altamente alinhada ao seu futuro Cloud/IA."
        cor_veredicto = GREEN
    elif pts_sys >= 4:
        if pts_drain <= -3:
            veredicto = "TIER 2 com Risco (Sponsor/Atenção) - Vaga de Sistemas com pedágio de Front-end."
            cor_veredicto = YELLOW
        else:
            veredicto = "TIER 2 (Sponsor) - Vaga sólida de Sistemas/Backend."
            cor_veredicto = CYAN
    else:
        veredicto = "INCONCLUSIVO / OUTRO PERFIL"
        cor_veredicto = RESET

    # Impressão do Relatório
    print(f"\n{BOLD}=== REALITY CHECK FILTER: RELATÓRIO ANALÍTICO ==={RESET}")
    print(f"Arquivo analisado: {file_path}")
    print(f"Score Total: {BOLD}{pontuacao_total} pontos{RESET}\n")

    for categoria, info in VETORES.items():
        cor = GREEN if info["peso"] > 0 else RED
        
        # Formata a string de encontrados com a frequência ex: "linux (3x)"
        itens_list = [f"{palavra}({qtd}x)" for palavra, qtd in resultados[categoria]["encontradas"].items()]
        itens = ", ".join(itens_list) if itens_list else "Nenhuma"
        
        pts = resultados[categoria]["pontos"]
        print(f"{cor}{info['nome']}{RESET}")
        print(f"Pontos acumulados: {pts}")
        print(f"Densidade de palavras: {itens}\n")

    print(f"{BOLD}--- VETORES SECUNDÁRIOS (Dados Extraídos) ---{RESET}")
    for cat, encontrados in secundarios_encontrados.items():
        valores = ", ".join(encontrados) if encontrados else "Não especificado"
        print(f"{cat.capitalize()}: {valores}")

    print(f"\n{BOLD}=== VEREDICTO ARQUITETURAL ==={RESET}")
    print(f"{cor_veredicto}{BOLD}{veredicto}{RESET}\n")

    # Coleta de dados para CSV
    csv_data = {
        'arquivo': file_path,
        'score_total': pontuacao_total,
        'score_cloud': pts_cloud,
        'score_sys': pts_sys,
        'score_drain': pts_drain,
        'veredicto': veredicto.split(" - ")[0], # Pega apenas a sigla curta
        'sec_senioridade': "|".join(secundarios_encontrados["SENIORIDADE"]),
        'sec_metodologia': "|".join(secundarios_encontrados["METODOLOGIA"]),
        'sec_modelo': "|".join(secundarios_encontrados["MODELO_TRABALHO"]),
        'termos_cloud': ",".join([f"{p}({q})" for p,q in resultados["TIER_1_CLOUD"]["encontradas"].items()]),
        'termos_sys': ",".join([f"{p}({q})" for p,q in resultados["TIER_2_SYSTEMS"]["encontradas"].items()]),
        'termos_drain': ",".join([f"{p}({q})" for p,q in resultados["TIER_3_DRAINERS"]["encontradas"].items()]),
    }
    
    save_to_csv(csv_data)
    print(f"{CYAN}>> Log gravado com sucesso em '{CSV_FILE}' para análise futura.{RESET}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <caminho_para_arquivo_da_vaga.txt>")
        sys.exit(1)
    analyze_job(sys.argv[1])
