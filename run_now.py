#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================
OmniRoute - Execução Manual de Prospecção
=============================================================
Executa um ciclo de prospecção imediatamente, sem esperar
pelo agendador. Útil para testes e buscas sob demanda.

Uso:
    python3 run_now.py              # Executa com configurações padrão
    python3 run_now.py --qtd 50     # Busca 50 leads
    python3 run_now.py --cidade SP  # Apenas São Paulo
    python3 run_now.py --abrir      # Abre a pasta de leads após execução
=============================================================
"""

import os
import sys
import argparse
import subprocess
import platform
from datetime import datetime

# Diretórios
DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_LEADS = os.path.join(DIR_BASE, "leads")
DIR_LOGS = os.path.join(DIR_BASE, "logs")

# Cores ANSI
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
NEGRITO = "\033[1m"
RESET = "\033[0m"


def cor(texto, cor_ansi):
    """Aplica cor ANSI ao texto."""
    return f"{cor_ansi}{texto}{RESET}"


def abrir_pasta(caminho):
    """Abre a pasta no Finder (macOS)."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["open", caminho], check=True)
        elif sistema == "Linux":
            subprocess.run(["xdg-open", caminho], check=True)
        elif sistema == "Windows":
            subprocess.run(["explorer", caminho], check=True)
        print(cor(f"📂 Pasta aberta: {caminho}", AZUL))
    except Exception as e:
        print(cor(f"⚠️  Não foi possível abrir a pasta: {e}", AMARELO))


def contar_csvs_hoje():
    """Conta quantos CSVs foram gerados hoje."""
    hoje = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(DIR_LEADS):
        return 0

    return sum(
        1 for f in os.listdir(DIR_LEADS)
        if f.endswith(".csv") and hoje in f
    )


def main():
    """Função principal — executa uma prospecção imediata."""

    # Parser de argumentos
    parser = argparse.ArgumentParser(
        description="OmniRoute - Execução manual de prospecção de leads"
    )
    parser.add_argument(
        "--qtd", type=int, default=None,
        help="Quantidade de leads a buscar (padrão: 30)"
    )
    parser.add_argument(
        "--cidade", type=str, default=None,
        choices=["bauru", "sp", "ambas"],
        help="Cidade alvo: bauru, sp, ou ambas (padrão: ambas)"
    )
    parser.add_argument(
        "--abrir", action="store_true",
        help="Abre a pasta de leads após a execução"
    )
    parser.add_argument(
        "--score-minimo", type=int, default=None,
        help="Score mínimo de validação (padrão: 50)"
    )

    args = parser.parse_args()

    # Banner
    print(f"""
{cor('=' * 60, CIANO)}
{cor('  🚀 OmniRoute - Prospecção Manual', CIANO + NEGRITO)}
{cor('  Edição de Vídeos de Posicionamento e Branding', AZUL)}
{cor('=' * 60, CIANO)}
""")

    # Info prévia
    csvs_hoje = contar_csvs_hoje()
    if csvs_hoje > 0:
        print(cor(f"📊 Já foram gerados {csvs_hoje} arquivo(s) de leads hoje.", AMARELO))

    agora = datetime.now()
    print(cor(f"⏰ Início: {agora.strftime('%d/%m/%Y %H:%M:%S')}", AZUL))
    print(cor(f"📂 Destino: {DIR_LEADS}", AZUL))
    print()

    # Cria diretório de leads se não existir
    os.makedirs(DIR_LEADS, exist_ok=True)
    os.makedirs(DIR_LOGS, exist_ok=True)

    # Importa o prospector
    if DIR_BASE not in sys.path:
        sys.path.insert(0, DIR_BASE)

    try:
        import prospector
    except ImportError as e:
        print(cor(f"❌ Erro ao importar prospector.py: {e}", VERMELHO))
        print(cor("   Verifique se o arquivo prospector.py existe no mesmo diretório.", AMARELO))
        sys.exit(1)

    # Aplica configurações personalizadas se fornecidas
    if args.qtd is not None and hasattr(prospector, "CONFIG"):
        prospector.CONFIG["leads_por_ciclo"] = args.qtd
    elif args.qtd is not None and hasattr(prospector, "LEADS_POR_CICLO"):
        prospector.LEADS_POR_CICLO = args.qtd

    if args.score_minimo is not None and hasattr(prospector, "CONFIG"):
        prospector.CONFIG["score_minimo"] = args.score_minimo
    elif args.score_minimo is not None and hasattr(prospector, "SCORE_MINIMO"):
        prospector.SCORE_MINIMO = args.score_minimo

    if args.cidade is not None and hasattr(prospector, "CONFIG"):
        if args.cidade == "bauru":
            prospector.CONFIG["cidades"] = ["Bauru"]
        elif args.cidade == "sp":
            prospector.CONFIG["cidades"] = ["São Paulo"]
        # "ambas" mantém o padrão

    # Executa a prospecção
    print(cor("🔍 Iniciando prospecção de leads...\n", CIANO + NEGRITO))

    inicio = datetime.now()

    try:
        # Tenta diferentes nomes de função principal
        if hasattr(prospector, "main"):
            resultado = prospector.main()
        elif hasattr(prospector, "executar_prospeccao"):
            resultado = prospector.executar_prospeccao()
        elif hasattr(prospector, "prospectar"):
            resultado = prospector.prospectar()
        else:
            print(cor("❌ Nenhuma função principal encontrada no prospector.py", VERMELHO))
            print(cor("   O prospector.py deve ter uma função main(), executar_prospeccao() ou prospectar().", AMARELO))
            sys.exit(1)
    except KeyboardInterrupt:
        print(cor("\n\n🛑 Prospecção cancelada pelo usuário.", AMARELO))
        sys.exit(0)
    except Exception as e:
        print(cor(f"\n❌ Erro durante a prospecção: {e}", VERMELHO))
        import traceback
        traceback.print_exc()
        sys.exit(1)

    fim = datetime.now()
    duracao = fim - inicio

    # Resumo
    print(f"\n{cor('=' * 60, CIANO)}")
    print(cor("  ✅ PROSPECÇÃO CONCLUÍDA", VERDE + NEGRITO))
    print(cor(f"  ⏱️  Duração: {duracao.seconds // 60}min {duracao.seconds % 60}s", AZUL))

    # Tenta extrair info do resultado
    if isinstance(resultado, dict):
        arquivo = resultado.get("arquivo", resultado.get("file", ""))
        qtd = resultado.get("total", resultado.get("quantidade", resultado.get("count", "?")))
        print(cor(f"  📊 Leads encontrados: {qtd}", VERDE))
        if arquivo:
            print(cor(f"  📁 Arquivo: {arquivo}", AZUL))
    elif isinstance(resultado, tuple) and len(resultado) >= 2:
        print(cor(f"  📁 Arquivo: {resultado[0]}", AZUL))
        print(cor(f"  📊 Leads: {resultado[1]}", VERDE))
    elif isinstance(resultado, str):
        print(cor(f"  📁 Arquivo: {resultado}", AZUL))

    # Procura o CSV mais recente
    arquivos_csv = sorted(
        [os.path.join(DIR_LEADS, f) for f in os.listdir(DIR_LEADS) if f.endswith(".csv")],
        key=os.path.getmtime,
        reverse=True
    )
    if arquivos_csv:
        mais_recente = arquivos_csv[0]
        tamanho = os.path.getsize(mais_recente)
        print(cor(f"  📄 Último CSV: {os.path.basename(mais_recente)} ({tamanho:,} bytes)", AZUL))

        # Conta linhas (leads) no CSV
        try:
            with open(mais_recente, "r", encoding="utf-8") as f:
                linhas = sum(1 for _ in f) - 1  # Subtrai header
            print(cor(f"  📊 Total de leads no arquivo: {linhas}", VERDE))
        except Exception:
            pass

    print(cor("=" * 60, CIANO))

    # Abre a pasta se solicitado
    if args.abrir:
        abrir_pasta(DIR_LEADS)
    else:
        print(cor(f"\n💡 Dica: use --abrir para abrir a pasta de leads automaticamente.", AMARELO))
        print(cor(f"   Ou acesse: {DIR_LEADS}", AZUL))


if __name__ == "__main__":
    main()
