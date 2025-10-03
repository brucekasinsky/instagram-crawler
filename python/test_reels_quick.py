#!/usr/bin/env python3
"""
Teste Rápido - Coleta dos Primeiros Reels
Para conferir os números de views, likes e comments
"""
import instaloader
from config import PROXY_CONFIG
import sys

print("🧪 Teste Rápido - Primeiros Reels do Felipe Neto")
print("=" * 50)

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
    print(f"   Posts: {profile.mediacount}")
except Exception as e:
    print(f"❌ Erro ao carregar perfil: {e}")
    sys.exit(1)

print("\n📹 Coletando os primeiros reels...")
print("=" * 50)

reels_collected = 0
max_reels = 10  # Coletar apenas os primeiros 10 reels

try:
    posts_generator = profile.get_posts()
    
    for post in posts_generator:
        if reels_collected >= max_reels:
            break
            
        # Verificar se é reel (GraphVideo)
        if getattr(post, 'typename', '') == 'GraphVideo':
            reels_collected += 1
            
            # Coletar dados
            likes = getattr(post, 'likes', 0) or 0
            comments = getattr(post, 'comments', 0) or 0
            views = getattr(post, 'video_view_count', 0) or 0
            date = getattr(post, 'date_utc', None)
            shortcode = getattr(post, 'shortcode', '')
            
            # Formatar números
            def format_number(num):
                if num >= 1000000:
                    return f"{num/1000000:.1f}M"
                elif num >= 1000:
                    return f"{num/1000:.1f}K"
                else:
                    return str(num)
            
            print(f"📹 REEL {reels_collected}:")
            print(f"   Likes: {format_number(likes)} ({likes:,})")
            print(f"   Views: {format_number(views)} ({views:,})")
            print(f"   Comments: {format_number(comments)} ({comments:,})")
            print(f"   Data: {date}")
            print(f"   Shortcode: {shortcode}")
            print("-" * 30)
            
except Exception as e:
    print(f"❌ Erro durante coleta: {e}")

print(f"\n✅ Total de reels coletados: {reels_collected}")
print("\n🔍 Agora você pode conferir esses números no Instagram!")
print("   Os reels devem estar ordenados dos mais novos para os mais antigos.")
