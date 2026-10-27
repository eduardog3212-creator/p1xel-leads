#!/bin/bash
# Script de execução rápida para o sistema de prospecção

cd /Users/eduardog/Desktop/omniroute

# Menu de opções
echo "=================================="
echo "🎬 EduardoOG - Gerador de Leads"
echo "=================================="
echo "1) Buscar leads agora"
echo "2) Iniciar scheduler (8h, 12h, 18h)"
echo "3) Ver leads do dia"
echo "4) Sair"
echo ""
read -p "Escolha uma opção: " opcao

case $opcao in
  1)
    echo "🚀 Executando prospecção..."
    python3 prospector.py
    ;;
  2)
    echo "⏰ Iniciando scheduler..."
    python3 scheduler.py
    ;;
  3)
    echo "📋 Leads de hoje:"
    ls -la leads/ | grep "$(date +%Y-%m-%d)"
    ;;
  4)
    echo "👋 Até mais!"
    exit 0
    ;;
  *)
    echo "❌ Opção inválida"
    exit 1
    ;;
esac