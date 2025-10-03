#!/usr/bin/env python3
"""
Teste Simples - Views Aprimorados
Baseado no que funcionou anteriormente
"""
import instaloader
from config import PROXY_CONFIG
import sys

print("🧪 Teste Simples - Views Aprimorados")
print("=" * 50)

# Initialize instaloader
L = instaloader.Instaloader()

# Configure proxy
session = L.context._session
session.proxies = {'http': PROXY_CONFIG['http'], 'https': PROXY_CONFIG['https']}

# Load profile
profile = instaloader.Profile.from_username(L.context, "felipeneto")
print(f"✅ Perfil: {profile.username}")

def get_enhanced_views(post):
    """Tenta obter views de diferentes campos"""
    view_fields = [
        'video_view_count',
        'view_count', 
        'views',
        'play_count',
        'video_play_count'
    ]
    
    max_views = 0
    best_field = None
    
    for field in view_fields:
        try:
            value = getattr(post, field, 0) or 0
            if value > max_views:
                max_views = value
                best_field = field
        except:
            continue
    
    return max_views, best_field

print("\n📹 Testando views aprimorados nos primeiros reels...")
print("=" * 50)

reels_collected = 0
max_reels = 5

try:
    posts_generator = profile.get_posts()
    
    for post in posts_generator:
        if reels_collected >= max_reels:
            break
            
        if getattr(post, 'typename', '') == 'GraphVideo':
            reels_collected += 1
            
            # Dados básicos
            likes = getattr(post, 'likes', 0) or 0
            comments = getattr(post, 'comments', 0) or 0
            shortcode = getattr(post, 'shortcode', '')
            
            # Views aprimorados
            enhanced_views, best_field = get_enhanced_views(post)
            
            # Views padrão para comparação
            standard_views = getattr(post, 'video_view_count', 0) or 0
            
            def format_number(num):
                if num >= 1000000:
                    return f"{num/1000000:.1f}M"
                elif num >= 1000:
                    return f"{num/1000:.1f}K"
                else:
                    return str(num)
            
            print(f"📹 REEL {reels_collected}:")
            print(f"   Shortcode: {shortcode}")
            print(f"   Likes: {format_number(likes)} ({likes:,})")
            print(f"   Comments: {format_number(comments)} ({comments:,})")
            print(f"   Views (padrão): {format_number(standard_views)} ({standard_views:,})")
            print(f"   Views (aprimorado): {format_number(enhanced_views)} ({enhanced_views:,})")
            print(f"   Campo usado: {best_field}")
            print("-" * 40)
            
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n✅ Teste concluído - {reels_collected} reels analisados")



