#!/usr/bin/env python3
"""
Instagram Hybrid Scraper - Combina instaloader com correção de views
"""
import instaloader
import requests
import re
import json
from config import PROXY_CONFIG

def get_correct_views_from_shortcode(shortcode):
    """
    Tenta obter os views corretos diretamente do post individual
    """
    try:
        url = f"https://www.instagram.com/p/{shortcode}/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        }
        
        response = requests.get(url, headers=headers, proxies=PROXY_CONFIG, timeout=10)
        
        if response.status_code == 200:
            # Procurar por views no HTML
            view_patterns = [
                r'"video_view_count":(\d+)',
                r'"view_count":(\d+)',
                r'"views":(\d+)',
                r'(\d+[,.]?\d*)\s*mi\s*visualizações',
                r'(\d+[,.]?\d*)\s*mi\s*views'
            ]
            
            for pattern in view_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    # Pegar o maior número encontrado
                    max_views = max([int(match.replace(',', '').replace('.', '')) for match in matches])
                    if max_views > 100000:  # Só aceitar se for um número razoável
                        return max_views
        
        return None
        
    except Exception as e:
        print(f"⚠️ Erro ao obter views do {shortcode}: {e}")
        return None

def scrape_reels_with_correct_views():
    """
    Scraping híbrido: instaloader + correção de views
    """
    print("🎯 Instagram Hybrid Scraper - Reels com Views Corretos")
    print("=" * 60)
    
    # Initialize instaloader
    L = instaloader.Instaloader()
    
    # Configure proxy
    print("🌐 Configurando proxy...")
    session = L.context._session
    session.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    # Load profile
    print("🔍 Carregando perfil...")
    try:
        profile = instaloader.Profile.from_username(L.context, "felipeneto")
        print(f"✅ Perfil carregado: {profile.username}")
        print(f"   Seguidores: {profile.followers:,}")
    except Exception as e:
        print(f"❌ Erro ao carregar perfil: {e}")
        return
    
    print("\n📹 Coletando reels com views corretos...")
    print("=" * 60)
    
    reels_collected = 0
    max_reels = 12
    
    try:
        posts_generator = profile.get_posts()
        
        for post in posts_generator:
            if reels_collected >= max_reels:
                break
                
            # Verificar se é reel (GraphVideo)
            if getattr(post, 'typename', '') == 'GraphVideo':
                reels_collected += 1
                
                # Dados básicos do instaloader
                shortcode = getattr(post, 'shortcode', '')
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                views_instaloader = getattr(post, 'video_view_count', 0) or 0
                date = getattr(post, 'date_utc', None)
                
                print(f"📹 REEL {reels_collected}:")
                print(f"   Shortcode: {shortcode}")
                print(f"   Likes: {likes:,}")
                print(f"   Comments: {comments:,}")
                print(f"   Views (instaloader): {views_instaloader:,}")
                
                # Tentar obter views corretos
                print(f"   🔍 Buscando views corretos...")
                correct_views = get_correct_views_from_shortcode(shortcode)
                
                if correct_views:
                    print(f"   ✅ Views corretos: {correct_views:,}")
                    views_final = correct_views
                else:
                    print(f"   ⚠️ Usando views do instaloader: {views_instaloader:,}")
                    views_final = views_instaloader
                
                # Formatar para exibição
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📊 RESULTADO FINAL:")
                print(f"      Likes: {format_number(likes)} ({likes:,})")
                print(f"      Views: {format_number(views_final)} ({views_final:,})")
                print(f"      Comments: {format_number(comments)} ({comments:,})")
                print(f"      Data: {date}")
                print("-" * 50)
                
    except Exception as e:
        print(f"❌ Erro durante coleta: {e}")
    
    print(f"\n✅ Total de reels coletados: {reels_collected}")

if __name__ == "__main__":
    scrape_reels_with_correct_views()



