# 🎬 EduardoOG - Sistema de Prospecção de Leads

Sistema automatizado para buscar clientes potenciais para serviços de vídeo de posicionamento e branding.

## 📋 O que foi criado

| Arquivo | Função |
|---------|--------|
| `prospector.py` | Motor de busca de leads |
| `scheduler.py` | Agendador manual (alternativa ao cron) |
| `setup_cron.sh` | Configura execução automática via cron |
| `run.sh` | Menu de execução rápida |
| `leads/` | Pasta onde os CSVs são salvos |

## 🚀 Como usar

### Executar agora (busca manual):
```bash
cd /Users/eduardog/Desktop/omniroute
python3 prospector.py
```

### Configurar execução automática:
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

Isso configura o cron para rodar às **8h, 12h e 18h** todos os dias.

### Ver leads do dia:
```bash
ls -la leads/
```

## 📊 Formato do CSV

| Coluna | Descrição |
|--------|-----------|
| Nome | Nome do lead |
| Nicho | Categoria (profissionais_marca_pessoal, negocios_locais, etc.) |
| Cidade | Bauru ou São Paulo |
| Website | URL do site |
| Telefone | Telefone (se encontrado) |
| Email | Email (se encontrado) |
| Instagram | Perfil do Instagram |
| LinkedIn | Perfil do LinkedIn |
| Facebook | Página do Facebook |
| Score | Pontuação de validação (0-100) |
| Notas | Observações sobre o lead |
| Data_encontro | Data/hora da captura |

## ⚙️ Configuração

Edite o dicionário `CONFIG` no início de `prospector.py` para ajustar:

- `leads_por_busca`: Quantidade de leads por execução (padrão: 30)
- `cidades`: Cidades de busca
- `min_score`: Pontuação mínima para incluir lead (padrão: 50)
- `min_delay` / `max_delay`: Intervalo entre requisições

## ⚠️ Limitações

- Busca em fontes públicas (não tem acesso a bases pagas como Apollo/Lusha)
- Depende de resultados disponíveis no DuckDuckGo
- Algumas requisições podem ser bloqueadas (rate limiting)
- Recomenda-se usar VPN ou proxy se houver muitos bloqueios