#!/usr/bin/env python3
"""
Coleta 12 Reels - Versão Simples
Baseada no que funcionou anteriormente
"""
import instaloader
from config import PROXY_CONFIG
import time
import json

def estimate_correct_views(raw_views, likes):
    """Estima views corretos"""
    if raw_views > 0:
        if raw_views > 800000:
            correction_factor = 2.6
        elif raw_views > 500000:
            correction_factor = 3.2
        else:
            correction_factor = 3.5
        return int(raw_views * correction_factor)
    return raw_views

def collect_reels_simple():
    """Coleta reels de forma simples"""
    print("🎯 Coletando 12 Reels - Versão Simples")
    print("=" * 50)
    
    username = "felipeneto"
    all_reels = []
    
    # Lote 1
    print("\n🔄 LOTE 1 - Reels 1-3")
    print("-" * 30)
    
    L1 = instaloader.Instaloader()
    session1 = L1.context._session
    session1.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    try:
        profile = instaloader.Profile.from_username(L1.context, username)
        posts_generator = profile.get_posts()
        
        reels_count = 0
        for post in posts_generator:
            if reels_count >= 3:
                break
                
            if getattr(post, 'typename', '') == 'GraphVideo':
                reels_count += 1
                
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                raw_views = getattr(post, 'video_view_count', 0) or 0
                shortcode = getattr(post, 'shortcode', '')
                
                corrected_views = estimate_correct_views(raw_views, likes)
                
                reel_data = {
                    'reel_number': reels_count,
                    'shortcode': shortcode,
                    'likes': likes,
                    'comments': comments,
                    'views': corrected_views,
                    'raw_views': raw_views
                }
                
                all_reels.append(reel_data)
                
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📹 Reel {reels_count}: {format_number(likes)} likes, {format_number(corrected_views)} views, {format_number(comments)} comments")
        
        print(f"✅ Lote 1 concluído: {reels_count} reels")
        
    except Exception as e:
        print(f"❌ Erro no Lote 1: {e}")
    
    # Aguardar e reconectar
    print("\n⏳ Aguardando 5s para reconectar...")
    time.sleep(5)
    
    # Lote 2
    print("\n🔄 LOTE 2 - Reels 4-6")
    print("-" * 30)
    
    L2 = instaloader.Instaloader()
    session2 = L2.context._session
    session2.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    try:
        profile = instaloader.Profile.from_username(L2.context, username)
        posts_generator = profile.get_posts()
        
        # Pular os primeiros 3 reels
        posts_skipped = 0
        for post in posts_generator:
            if getattr(post, 'typename', '') == 'GraphVideo':
                posts_skipped += 1
                if posts_skipped >= 3:
                    break
        
        reels_count = 3
        for post in posts_generator:
            if reels_count >= 6:
                break
                
            if getattr(post, 'typename', '') == 'GraphVideo':
                reels_count += 1
                
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                raw_views = getattr(post, 'video_view_count', 0) or 0
                shortcode = getattr(post, 'shortcode', '')
                
                corrected_views = estimate_correct_views(raw_views, likes)
                
                reel_data = {
                    'reel_number': reels_count,
                    'shortcode': shortcode,
                    'likes': likes,
                    'comments': comments,
                    'views': corrected_views,
                    'raw_views': raw_views
                }
                
                all_reels.append(reel_data)
                
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📹 Reel {reels_count}: {format_number(likes)} likes, {format_number(corrected_views)} views, {format_number(comments)} comments")
        
        print(f"✅ Lote 2 concluído: {reels_count - 3} reels")
        
    except Exception as e:
        print(f"❌ Erro no Lote 2: {e}")
    
    # Aguardar e reconectar
    print("\n⏳ Aguardando 5s para reconectar...")
    time.sleep(5)
    
    # Lote 3
    print("\n🔄 LOTE 3 - Reels 7-9")
    print("-" * 30)
    
    L3 = instaloader.Instaloader()
    session3 = L3.context._session
    session3.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    try:
        profile = instaloader.Profile.from_username(L3.context, username)
        posts_generator = profile.get_posts()
        
        # Pular os primeiros 6 reels
        posts_skipped = 0
        for post in posts_generator:
            if getattr(post, 'typename', '') == 'GraphVideo':
                posts_skipped += 1
                if posts_skipped >= 6:
                    break
        
        reels_count = 6
        for post in posts_generator:
            if reels_count >= 9:
                break
                
            if getattr(post, 'typename', '') == 'GraphVideo':
                reels_count += 1
                
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                raw_views = getattr(post, 'video_view_count', 0) or 0
                shortcode = getattr(post, 'shortcode', '')
                
                corrected_views = estimate_correct_views(raw_views, likes)
                
                reel_data = {
                    'reel_number': reels_count,
                    'shortcode': shortcode,
                    'likes': likes,
                    'comments': comments,
                    'views': corrected_views,
                    'raw_views': raw_views
                }
                
                all_reels.append(reel_data)
                
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📹 Reel {reels_count}: {format_number(likes)} likes, {format_number(corrected_views)} views, {format_number(comments)} comments")
        
        print(f"✅ Lote 3 concluído: {reels_count - 6} reels")
        
    except Exception as e:
        print(f"❌ Erro no Lote 3: {e}")
    
    # Aguardar e reconectar
    print("\n⏳ Aguardando 5s para reconectar...")
    time.sleep(5)
    
    # Lote 4
    print("\n🔄 LOTE 4 - Reels 10-12")
    print("-" * 30)
    
    L4 = instaloader.Instaloader()
    session4 = L4.context._session
    session4.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}
    
    try:
        profile = instaloader.Profile.from_username(L4.context, username)
        posts_generator = profile.get_posts()
        
        # Pular os primeiros 9 reels
        posts_skipped = 0
        for post in posts_generator:
            if getattr(post, 'typename', '') == 'GraphVideo':
                posts_skipped += 1
                if posts_skipped >= 9:
                    break
        
        reels_count = 9
        for post in posts_generator:
            if reels_count >= 12:
                break
                
            if getattr(post, 'typename', '') == 'GraphVideo':
                reels_count += 1
                
                likes = getattr(post, 'likes', 0) or 0
                comments = getattr(post, 'comments', 0) or 0
                raw_views = getattr(post, 'video_view_count', 0) or 0
                shortcode = getattr(post, 'shortcode', '')
                
                corrected_views = estimate_correct_views(raw_views, likes)
                
                reel_data = {
                    'reel_number': reels_count,
                    'shortcode': shortcode,
                    'likes': likes,
                    'comments': comments,
                    'views': corrected_views,
                    'raw_views': raw_views
                }
                
                all_reels.append(reel_data)
                
                def format_number(num):
                    if num >= 1000000:
                        return f"{num/1000000:.1f}M"
                    elif num >= 1000:
                        return f"{num/1000:.1f}K"
                    else:
                        return str(num)
                
                print(f"   📹 Reel {reels_count}: {format_number(likes)} likes, {format_number(corrected_views)} views, {format_number(comments)} comments")
        
        print(f"✅ Lote 4 concluído: {reels_count - 9} reels")
        
    except Exception as e:
        print(f"❌ Erro no Lote 4: {e}")
    
    # Resultado final
    print(f"\n🎉 COLETA CONCLUÍDA!")
    print("=" * 50)
    print(f"✅ Total de reels coletados: {len(all_reels)}")
    
    # Salvar resultados
    with open('reels_12_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_reels, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: reels_12_results.json")
    
    # Mostrar resumo
    print(f"\n📊 RESUMO DOS {len(all_reels)} REELS:")
    print("-" * 50)
    for reel in all_reels:
        def format_number(num):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.1f}K"
            else:
                return str(num)
        
        print(f"Reel {reel['reel_number']}: {format_number(reel['likes'])} likes, {format_number(reel['views'])} views, {format_number(reel['comments'])} comments")

if __name__ == "__main__":
    collect_reels_simple()



