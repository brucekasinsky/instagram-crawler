#!/usr/bin/env python3
"""
Debug Views - Verificar todos os campos de views disponíveis
"""
import instaloader
from config import PROXY_CONFIG
import sys

print("🔍 Debug Views - Verificando todos os campos disponíveis")
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
except Exception as e:
    print(f"❌ Erro ao carregar perfil: {e}")
    sys.exit(1)

print("\n📹 Analisando campos de views do primeiro reel...")
print("=" * 60)

try:
    posts_generator = profile.get_posts()
    
    for post in posts_generator:
        # Verificar se é reel (GraphVideo)
        if getattr(post, 'typename', '') == 'GraphVideo':
            print("🔍 PRIMEIRO REEL ENCONTRADO:")
            print(f"   Shortcode: {getattr(post, 'shortcode', 'N/A')}")
            print(f"   Data: {getattr(post, 'date_utc', 'N/A')}")
            print()
            
            # Verificar todos os campos relacionados a views
            print("📊 CAMPOS DE VIEWS DISPONÍVEIS:")
            print("-" * 40)
            
            # Campos conhecidos
            fields_to_check = [
                'video_view_count',
                'view_count', 
                'views',
                'play_count',
                'video_play_count',
                'impressions',
                'reach',
                'video_views',
                'total_views',
                'viewer_count'
            ]
            
            for field in fields_to_check:
                value = getattr(post, field, 'N/A')
                print(f"   {field}: {value}")
            
            print()
            print("📋 TODOS OS ATRIBUTOS DO POST:")
            print("-" * 40)
            
            # Listar todos os atributos
            all_attrs = dir(post)
            view_related = [attr for attr in all_attrs if 'view' in attr.lower() or 'play' in attr.lower() or 'count' in attr.lower()]
            
            for attr in view_related:
                try:
                    value = getattr(post, attr)
                    print(f"   {attr}: {value}")
                except:
                    print(f"   {attr}: <erro ao acessar>")
            
            print()
            print("📊 OUTROS DADOS IMPORTANTES:")
            print("-" * 40)
            print(f"   Likes: {getattr(post, 'likes', 'N/A')}")
            print(f"   Comments: {getattr(post, 'comments', 'N/A')}")
            print(f"   Typename: {getattr(post, 'typename', 'N/A')}")
            print(f"   Is Video: {getattr(post, 'is_video', 'N/A')}")
            print(f"   Video Duration: {getattr(post, 'video_duration', 'N/A')}")
            
            break  # Só analisar o primeiro reel
            
except Exception as e:
    print(f"❌ Erro durante análise: {e}")

print("\n✅ Análise concluída!")



