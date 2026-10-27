#!/bin/bash
# Configura o cron para executar a prospecção automaticamente
# Rodar: chmod +x setup_cron.sh && ./setup_cron.sh

CRON_DIR="/Users/eduardog/Desktop/omniroute"
PROSPECTOR="$CRON_DIR/prospector.py"
PYTHON="/usr/bin/python3"

echo "======================================"
echo "⏰ Configurando Cron para EduardoOG"
echo "======================================"
echo ""

# Remove crontab existente do EduardoOG (se houver)
crontab -l 2>/dev/null | grep -v "prospector.py" > /tmp/minha_cron_temp

# Adiciona as novas entradas
cat >> /tmp/minha_cron_temp << 'EOF'
# EduardoOG - Prospecção de Leads (8h, 12h, 18h)
0 8 * * * /usr/bin/python3 /Users/eduardog/Desktop/omniroute/prospector.py >> /Users/eduardog/Desktop/omniroute/logs/cron_8h.log 2>&1
0 12 * * * /usr/bin/python3 /Users/eduardog/Desktop/omniroute/prospector.py >> /Users/eduardog/Desktop/omniroute/logs/cron_12h.log 2>&1
0 18 * * * /usr/bin/python3 /Users/eduardog/Desktop/omniroute/prospector.py >> /Users/eduardog/Desktop/omniroute/logs/cron_18h.log 2>&1
EOF

# Instala o novo crontab
crontab /tmp/minha_cron_temp
rm /tmp/minha_cron_temp

echo "✅ Cron configurado!"
echo ""
echo "Horários configurados:"
echo "  • 08:00 - leads_manhã.csv"
echo "  • 12:00 - leads_tarde.csv"
echo "  • 18:00 - leads_noite.csv"
echo ""
echo "Logs em: /Users/eduardog/Desktop/omniroute/logs/"
echo ""
echo "Para verificar o cron: crontab -l"
echo "Para remover: crontab -r"