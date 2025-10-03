#!/usr/bin/env python3
"""
Instagram HTML Scraper - Scraping direto do HTML
Para capturar os views corretos que estão no HTML da página
"""
import requests
import re
import json
from bs4 import BeautifulSoup
from config import PROXY_CONFIG

def scrape_instagram_reels_html(username):
    """
    Scraping direto do HTML da página de reels do Instagram
    """
    print(f"🔍 Scraping HTML da página de reels: {username}")
    
    # URL da página de reels
    url = f"https://www.instagram.com/{username}/reels/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("🌐 Fazendo requisição para a página de reels...")
        response = requests.get(url, headers=headers, proxies=PROXY_CONFIG, timeout=30)
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso!")
            
            # Parse do HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procurar por elementos que contenham views
            print("🔍 Procurando elementos de views no HTML...")
            
            # Procurar por spans que contenham "mi" (milhões)
            view_elements = soup.find_all('span', string=re.compile(r'\d+[,.]?\d*\s*mi'))
            
            print(f"📊 Encontrados {len(view_elements)} elementos com views em milhões:")
            
            reels_data = []
            for i, element in enumerate(view_elements[:12]):  # Primeiros 12 reels
                view_text = element.get_text().strip()
                print(f"   Reel {i+1}: {view_text}")
                
                # Extrair número
                view_match = re.search(r'(\d+[,.]?\d*)\s*mi', view_text)
                if view_match:
                    view_number = float(view_match.group(1).replace(',', '.'))
                    view_count = int(view_number * 1000000)  # Converter para número
                    
                    reels_data.append({
                        'reel_number': i+1,
                        'views_text': view_text,
                        'views_count': view_count,
                        'views_formatted': f"{view_number}M"
                    })
            
            return reels_data
            
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return []

def main():
    print("🎯 Instagram HTML Scraper - Views dos Reels")
    print("=" * 50)
    
    username = "felipeneto"
    reels_data = scrape_instagram_reels_html(username)
    
    if reels_data:
        print(f"\n✅ Coletados {len(reels_data)} reels:")
        print("=" * 50)
        
        for reel in reels_data:
            print(f"📹 Reel {reel['reel_number']}:")
            print(f"   Views: {reel['views_formatted']} ({reel['views_count']:,})")
            print(f"   Texto original: {reel['views_text']}")
            print("-" * 30)
    else:
        print("❌ Nenhum dado coletado")

if __name__ == "__main__":
    main()



