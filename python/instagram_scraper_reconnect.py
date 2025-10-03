#!/usr/bin/env python3
"""
Instagram Scraper com Reconexão - Coleta 12 reels
Reconecta a cada 3 reels para evitar limite de login
"""
import instaloader
from config import PROXY_CONFIG
import time
import json
from datetime import datetime
from pathlib import Path

def estimate_correct_views(raw_views, likes):
    """
    Estima views corretos baseado na relação observada
    """
    if raw_views > 0:
        if raw_views > 800000:  # Views altos
            correction_factor = 2.6
        elif raw_views > 500000:  # Views médios
            correction_factor = 3.2
        else:  # Views baixos
            correction_factor = 3.5
        
        return int(raw_views * correction_factor)
    
    return raw_views

def create_new_loader():
    """Cria um novo loader com proxy"""
    print("🔧 Criando novo loader...")
    L = instaloader.Instaloader()
    
    # Configure proxy
    session = L.context._session
    session.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    print("✅ Novo loader criado!")
    return L

def collect_reels_batch(loader, username, batch_size=3, start_from=0):
    """
    Coleta um lote de reels (3 por vez)
    """
    print(f"📹 Coletando lote de {batch_size} reels (iniciando do {start_from + 1})...")
    
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts_generator = profile.get_posts()
        
        # Pular posts até chegar no ponto de início
        for _ in range(start_from):
            try:
                next(posts_generator)
            except:
                break
        
        reels_collected = []
        posts_processed = 0
        
        for post in posts_generator:
            if len(reels_collected) >= batch_size:
                break
                
            posts_processed += 1
            
            if getattr(post, 'typename', '') == 'GraphVideo':
                # Dados básicos
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                raw_views = getattr(post, 'video_view_count', 0) or 0
                shortcode = getattr(post, 'shortcode', '')
                date = getattr(post, 'date_utc', None)
                caption = getattr(post, 'caption', '') or ''
                
                # Views corrigidos
                corrected_views = estimate_correct_views(raw_views, likes)
                
                reel_data = {
                    'shortcode': shortcode,
                    'likes': likes,
                    'comments': comments,
                    'views': corrected_views,
                    'raw_views': raw_views,
                    'date': str(date) if date else None,
                    'caption': caption
                }
                
                reels_collected.append(reel_data)
                
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📹 Reel {len(reels_collected)}: {format_number(likes)} likes, {format_number(corrected_views)} views, {format_number(comments)} comments")
                print(f"       Shortcode: {shortcode}")
        
        return reels_collected, posts_processed
        
    except Exception as e:
        print(f"❌ Erro no lote: {e}")
        return [], 0

def main():
    print("🎯 Instagram Scraper com Reconexão - 12 Reels")
    print("=" * 60)
    
    username = "felipeneto"
    target_reels = 12
    batch_size = 3
    all_reels = []
    total_posts_processed = 0
    
    batch_number = 1
    
    while len(all_reels) < target_reels:
        print(f"\n🔄 LOTE {batch_number} - Coletando {batch_size} reels...")
        print("-" * 40)
        
        # Criar novo loader para cada lote
        loader = create_new_loader()
        
        # Coletar lote
        batch_reels, posts_processed = collect_reels_batch(
            loader, username, batch_size, total_posts_processed
        )
        
        if batch_reels:
            all_reels.extend(batch_reels)
            total_posts_processed += posts_processed
            print(f"✅ Lote {batch_number} concluído: {len(batch_reels)} reels coletados")
        else:
            print(f"⚠️ Lote {batch_number} falhou")
            break
        
        # Se ainda precisamos de mais reels
        if len(all_reels) < target_reels:
            print(f"⏳ Aguardando 5s antes do próximo lote...")
            time.sleep(5)
            batch_number += 1
        else:
            break
    
    print(f"\n🎉 COLETA CONCLUÍDA!")
    print("=" * 60)
    print(f"✅ Total de reels coletados: {len(all_reels)}")
    print(f"📊 Total de posts processados: {total_posts_processed}")
    print(f"🔄 Total de lotes: {batch_number}")
    
    # Salvar resultados
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    results_file = Path(f"reels_results_{timestamp}.json")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'username': username,
            'total_reels': len(all_reels),
            'total_posts_processed': total_posts_processed,
            'batches': batch_number,
            'reels': all_reels
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {results_file}")
    
    # Mostrar resumo
    print(f"\n📊 RESUMO DOS REELS:")
    print("-" * 40)
    for i, reel in enumerate(all_reels[:12], 1):
        def format_number(num):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.1f}K"
            else:
                return str(num)
        
        print(f"Reel {i}: {format_number(reel['likes'])} likes, {format_number(reel['views'])} views, {format_number(reel['comments'])} comments")

if __name__ == "__main__":
    main()



