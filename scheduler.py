#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agendador de Prospecção - Executa o prospector nos horários definidos
Horário: 8h, 12h e 18h (segunda a segunda)
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Configuração de horários (formato 24h)
HORARIOS = [8, 12, 18]

# Caminho do prospector
PROSPECTOR_PATH = "/Users/eduardog/Desktop/omniroute/prospector.py"
LOG_DIR = "/Users/eduardog/Desktop/omniroute/logs"


def log(mensagem):
    """Log com timestamp"""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{agora}] {mensagem}")

    # Salvar em arquivo de log
    os.makedirs(LOG_DIR, exist_ok=True)
    nome_log = os.path.join(LOG_DIR, f"scheduler_{datetime.now().strftime('%Y-%m')}.log")
    with open(nome_log, "a", encoding="utf-8") as f:
        f.write(f"[{agora}] {mensagem}\n")


def executar_prospector():
    """Executa o script de prospecção"""
    try:
        log("🚀 Iniciando prospecção de leads...")

        resultado = subprocess.run(
            [sys.executable, PROSPECTOR_PATH],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos max
        )

        if resultado.returncode == 0:
            log("✅ Prospecção concluída com sucesso")
            if resultado.stdout:
                log(f"Saída: {resultado.stdout[:200]}")
        else:
            log(f"❌ Erro na prospecção: {resultado.stderr[:200]}")

    except subprocess.TimeoutExpired:
        log("❌ Timeout - prospecção demorou mais de 5 minutos")
    except Exception as e:
        log(f"❌ Erro ao executar: {e}")


def proximo_horario():
    """Retorna o próximo horário de execução"""
    agora = datetime.now()
    hora_atual = agora.hour

    for horario in HORARIOS:
        if horario > hora_atual:
            return horario

    # Se passou de todos, retorna o primeiro de amanhã
    return HORARIOS[0]


def tempo_ate_horario(horario):
    """Calcula segundos até o próximo horário"""
    agora = datetime.now()
    proximo = agora.replace(hour=horario, minute=0, second=0, microsecond=0)

    if horario <= agora.hour:
        proximo += timedelta(days=1)

    return (proximo - agora).total_seconds()


def main():
    """Loop principal do scheduler"""
    print("=" * 60)
    print("⏰ AGENDADOR DE PROSPECÇÃO - EduardoOG")
    print(f"   Horários: {', '.join(str(h) + 'h' for h in HORARIOS)}")
    print("=" * 60)
    print()

    # Primeira execução imediata para teste
    log("Iniciando scheduler...")

    while True:
        try:
            # Encontrar próximo horário
            horario_proximo = proximo_horario()
            segundos = tempo_ate_horario(horario_proximo)

            print(f"\n📅 Próxima execução: {horario_proximo}h (em {segundos/3600:.1f}h)")
            log(f"Aguardando até {horario_proximo}h ({segundos:.0f} segundos)")

            # Aguardar até o próximo horário
            time.sleep(segundos)

            # Verificar se é hora certa (com pequena margem)
            hora_atual = datetime.now().hour
            if hora_atual == horario_proximo:
                executar_prospector()
            else:
                log(f"⚠️ Pulou execução - hora atual: {hora_atual}")

            # Pequeno delay antes de calcular próximo horário
            time.sleep(10)

        except KeyboardInterrupt:
            log("Scheduler interrompido pelo usuário")
            break
        except Exception as e:
            log(f"Erro no loop: {e}")
            time.sleep(60)  # Espera 1min em caso de erro


def executar_agora():
    """Executa a prospecção agora mesmo (para teste)"""
    log("Execução manual solicitada")
    executar_prospector()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        executar_agora()
    else:
        main()