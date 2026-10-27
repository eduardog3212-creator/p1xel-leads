#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Prospecção de Leads - P1XEL Creative (OmniRoute)
Focado em pequenas/médias empresas e profissionais liberais locais reais em Bauru/SP e São Paulo Capital.
"""

import os
import re
import time
import random
import json
import csv
from datetime import datetime
from urllib.parse import quote_plus, unquote

import requests
from bs4 import BeautifulSoup
import pandas as pd

CONFIG = {
    "leads_por_busca": 30,
    "cidades": ["Bauru", "São Paulo"],
    "min_score": 50,
    "min_delay": 1,
    "max_delay": 2,
    "output_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads"),
    "timeout": 10,
}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

SEARCH_QUERIES = [
    "clínica estética Bauru SP instagram",
    "arquiteto Bauru SP instagram",
    "advogado São Paulo SP instagram",
    "psicólogo Bauru SP instagram",
    "espaço de beleza São Paulo SP instagram",
    "nutricionista clínica Bauru SP instagram"
]

MARCAS_GRANDES_BLOQUEADAS = [
    "coach", "senac", "fecaf", "natura", "merlin", "google", "facebook", "instagram",
    "wikipedia", "magazine luiza", "americanas", "shopee", "mercadolivre", "netflix",
    "spotify", "apple", "microsoft", "nike", "adidas", "zara", "starbucks", "mcdonalds",
    "youtube", "linkedin", "twitter"
]

TERMOS_BLOQUEADOS = [
    "10 melhores", "como ser", "o que é", "wikipedia", "top 20", "lista de",
    "significado", "salário", "quanto ganha", "vagas", "emprego", "curso",
    "faculdade", "livro", "artigo", "portal", "notícia", "guia", "pdf", "enciclopédia"
]

def gerar_mensagem_abertura(lead):
    primeiro_nome = lead.nome.split()[0] if lead.nome else "Olá"
    local = f" em {lead.cidade}" if lead.cidade else ""
    return f"Oi {primeiro_nome}! Acompanho seu trabalho{local} e vejo o quanto sua marca tem potencial. Notei que você ainda não investe em vídeos de posicionamento profissional para elevar seu ticket médio. Já pensou nisso?"

def gerar_mensagem_reuniao(lead):
    return "Que tal trocarmos 15 minutos de ideia pelo Zoom nesta semana? Posso te mostrar exemplos práticos de vídeos que produzi para negócios na sua região que geraram ótimos resultados. O que acha?"

class Lead:
    def __init__(self, nome, nicho, cidade, website="", telefone="", whatsapp="", instagram="", notas=""):
        self.nome = nome
        self.nicho = nicho
        self.cidade = cidade
        self.website = website
        self.telefone = telefone
        self.whatsapp = whatsapp
        self.instagram = instagram
        self.notas = notas
        self.score = 75
        self.data_encontrado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mensagem_abertura = ""
        self.mensagem_reuniao = ""

    def validar_e_pontuar(self):
        nome_lower = self.nome.lower()
        if any(t in nome_lower for t in TERMOS_BLOQUEADOS):
            return False
        if any(m in nome_lower for m in MARCAS_GRANDES_BLOQUEADAS):
            return False
        if len(self.nome.strip()) < 2:
            return False

        self.score = 90 if self.whatsapp else 75
        self.mensagem_abertura = gerar_mensagem_abertura(self)
        self.mensagem_reuniao = gerar_mensagem_reuniao(self)
        return True

    def to_dict(self):
        return {
            "Nome": self.nome,
            "Nicho": self.nicho,
            "Cidade": self.cidade,
            "Website": self.website,
            "Telefone": self.telefone,
            "WhatsApp": self.whatsapp,
            "Instagram": self.instagram,
            "Contato_Principal": self.whatsapp if self.whatsapp else self.instagram,
            "Score": self.score,
            "Mensagem_Abertura": self.mensagem_abertura,
            "Mensagem_Reuniao": self.mensagem_reuniao,
            "Notas": self.notas,
            "Data_encontrado": self.data_encontrado
        }


class Prospector:
    def __init__(self, config=CONFIG):
        self.config = config
        self.leads = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        })

    def delay(self):
        time.sleep(random.uniform(self.config["min_delay"], self.config["max_delay"]))

    def buscar_duckduckgo(self, query):
        resultados = []
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        try:
            self.delay()
            resp = self.session.post(url, data={"q": query}, timeout=self.config["timeout"])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for r in soup.select(".result"):
                    t = r.select_one(".result__title a")
                    snippet_el = r.select_one(".result__snippet")
                    if t:
                        nome = t.get_text(strip=True)
                        link = t.get("href", "")
                        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
                        resultados.append({"nome": nome, "link": link, "snippet": snippet})
        except Exception as e:
            print("Erro DuckDuckGo:", e)
        return resultados

    def executar(self):
        print("🚀 Iniciando prospecção via DuckDuckGo...")
        nomes_vistos = set()

        for query in SEARCH_QUERIES:
            if len(self.leads) >= self.config["leads_por_busca"]:
                break
            resps = self.buscar_duckduckgo(query)
            cidade = "Bauru" if "Bauru" in query else "São Paulo"
            nicho = "Negócio Local & Clínicas" if "clínica" in query or "estética" in query or "espaço" in query else "Profissional Liberal"

            for r in resps:
                if len(self.leads) >= self.config["leads_por_busca"]:
                    break
                nome = r["nome"]
                link = r["link"]
                snippet = r["snippet"]

                # Limpar nome
                nome = re.sub(r'\s*[-|]\s*.*$', '', nome)
                nome = re.sub(r'\s*\(.*\)$', '', nome)

                # Extrair Instagram
                instagram = ""
                combined = link + " " + snippet + " " + nome
                m_ig = re.search(r'instagram\.com/([a-zA-Z0-9_.]{3,30})', combined)
                if m_ig:
                    h = m_ig.group(1).strip('/')
                    if h.lower() not in ["p", "reel", "explore", "stories", "share", "login", "accounts"]:
                        instagram = f"https://instagram.com/{h}"
                else:
                    # Gerar um handle provável baseado no nome caso não venha no snippet direto
                    handle_limpo = re.sub(r'[^a-zA-Z0-9_]', '', nome.lower())
                    if len(handle_limpo) >= 3:
                        instagram = f"https://instagram.com/{handle_limpo[:20]}"

                # Extrair Telefone/WhatsApp
                whatsapp = ""
                telefone = ""
                tel_match = re.search(r'(?:\+?55\s?)?(?:\(?\d{2}\)?[\s.-]?)?\d{4,5}[\s.-]?\d{4}', snippet)
                if tel_match:
                    tel_limpo = re.sub(r'[^\d]', '', tel_match.group(0))
                    if len(tel_limpo) >= 10:
                        whatsapp = f"https://wa.me/55{tel_limpo}"
                        telefone = tel_match.group(0)

                lead = Lead(
                    nome=nome,
                    nicho=nicho,
                    cidade=cidade,
                    website=link if "http" in link else "",
                    telefone=telefone,
                    whatsapp=whatsapp,
                    instagram=instagram,
                    notas=snippet[:150]
                )

                if lead.validar_e_pontuar() and lead.nome.lower() not in nomes_vistos:
                    nomes_vistos.add(lead.nome.lower())
                    self.leads.append(lead)

        os.makedirs(self.config["output_dir"], exist_ok=True)
        agora = datetime.now()
        nome_arquivo = agora.strftime("leads_%Y-%m-%d_%Hh.csv")
        caminho = os.path.join(self.config["output_dir"], nome_arquivo)

        leads_data = [l.to_dict() for l in self.leads]
        df = pd.DataFrame(leads_data)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")

        self.gerar_html(leads_data)
        print(f"✅ Prospecção concluída! {len(self.leads)} leads salvos em {caminho}.")
        return caminho

    def gerar_html(self, dados):
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads_dashboard.html")
        if not os.path.exists(template_path):
            return
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        dados_json = json.dumps(dados, ensure_ascii=False, indent=2)
        script_update = f"let leads = {dados_json};\n        renderAll();"

        if "let leads = [" in content:
            content = re.sub(r'let leads\s*=\s*\[.*?\];', script_update, content, flags=re.DOTALL)

        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    p = Prospector()
    p.executar()
