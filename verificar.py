#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniRoute - Teste rápido do sistema
Verifica se tudo está instalado e funcionando.
"""

import sys
import os

def verificar():
    print("🔍 Verificando sistema OmniRoute...\n")

    erros = []

    # Verificar Python
    print(f"  ✅ Python {sys.version.split()[0]}")

    # Verificar dependências
    try:
        import requests
        print(f"  ✅ requests {requests.__version__}")
    except ImportError:
        erros.append("requests")
        print("  ❌ requests não instalado")

    try:
        import bs4
        print(f"  ✅ beautifulsoup4 {bs4.__version__}")
    except ImportError:
        erros.append("beautifulsoup4")
        print("  ❌ beautifulsoup4 não instalado")

    try:
        import pandas
        print(f"  ✅ pandas {pandas.__version__}")
    except ImportError:
        erros.append("pandas")
        print("  ❌ pandas não instalado")

    # Verificar diretórios
    base = os.path.dirname(os.path.abspath(__file__))

    leads_dir = os.path.join(base, "leads")
    if os.path.isdir(leads_dir):
        print(f"  ✅ Diretório leads/ existe")
    else:
        os.makedirs(leads_dir, exist_ok=True)
        print(f"  ⚠️  Diretório leads/ criado")

    logs_dir = os.path.join(base, "logs")
    if os.path.isdir(logs_dir):
        print(f"  ✅ Diretório logs/ existe")
    else:
        os.makedirs(logs_dir, exist_ok=True)
        print(f"  ⚠️  Diretório logs/ criado")

    # Verificar arquivos do sistema
    arquivos = ["prospector.py", "scheduler.py", "run_now.py", "setup_cron.sh"]
    for arq in arquivos:
        caminho = os.path.join(base, arq)
        if os.path.isfile(caminho):
            print(f"  ✅ {arq}")
        else:
            print(f"  ❌ {arq} não encontrado")
            erros.append(arq)

    print()

    if erros:
        print("⚠️  Problemas encontrados:")
        for e in erros:
            print(f"  - {e}")
        print("\nPara instalar dependências: pip3 install --user requests beautifulsoup4 pandas")
    else:
        print("✅ Tudo pronto! Execute: python3 run_now.py")

    return len(erros) == 0

if __name__ == "__main__":
    verificar()
